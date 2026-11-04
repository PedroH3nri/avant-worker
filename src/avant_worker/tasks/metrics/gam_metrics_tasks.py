"""Tarefas das métricas do Google Ad Manager (fila ``gam``).

- ``sync_metrics``: baixa os relatórios por ad unit e por key-value de uma network num
  período e grava com upsert pela chave natural (``store_gam_report`` do avant-core).
- ``schedule_metrics``: de hora em hora, ontem e hoje de cada network ativa. O dia de hoje
  é parcial e é regravado a cada hora.
- ``schedule_reprocess``: todo dia, os três dias antes de ontem, porque o GAM ajusta os
  números depois.
- ``backfill_metrics``: histórico de uma network nova, em lotes de 7 dias encadeados (um
  depois do outro), do mais novo para o mais antigo.

Com a trava da network ocupada, o lote volta para a fila daqui a um minuto em vez de ser
descartado: senão a sincronia e o reprocessamento da mesma network, ou dois lotes do
histórico, deixavam buracos sem erro.

Só networks com o inventário na própria network (M.A e conexão manual). As do MCM Manage
Inventory ficam na network da Groone e entram numa tarefa própria, que lê um relatório só
e distribui as linhas pelas Empresas.

Cada network roda com o Unit of Work da própria Empresa (RLS) e uma trava no Redis. Só os
``schedule_*`` usam ``trusted_uow``: listam as networks de todas as Empresas. Rodar duas
vezes grava o mesmo resultado.
"""

import logging
import time
import uuid
from datetime import date, timedelta
from typing import Any

from avant_core.gam.client.errors import GamError, GamUnavailable
from avant_core.gam.networks.enums import ConnectionType, Delegation
from avant_core.gam.networks.models import Network
from avant_core.gam.sync.services import sync_service
from avant_core.metrics.services import StoredMetrics, store_gam_report
from celery import chain

from avant_worker.adapters.events import METRICS_UPDATED, publish
from avant_worker.adapters.gam_reports import ReportKind
from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.metrics")

LOCK_SECONDS = 30 * 60

BACKFILL_DAYS = 90

BACKFILL_CHUNK_DAYS = 7

REPROCESS_DAYS = 3

# Com a network ocupada, tenta de novo a cada minuto por até duas horas.
LOCK_RETRY_SECONDS = 60

MAX_LOCK_ATTEMPTS = 120

RETRY_FOR = (GamUnavailable,)


@app.task(
    name="avant.gam.sync_metrics",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def sync_metrics(
    company_id: str, network_id: str, start: str, end: str, attempt: int = 0
) -> dict[str, Any]:
    """Grava as métricas da network entre ``start`` e ``end`` (datas ISO, inclusive)."""
    services = get_services()
    company_uuid, network_uuid = uuid.UUID(company_id), uuid.UUID(network_id)
    first_day, last_day = date.fromisoformat(start), date.fromisoformat(end)
    with services.lock(f"gam:metrics:{network_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return _network_busy(company_id, network_id, start, end, attempt)
        network = _network(services, company_uuid, network_uuid)
        if network is None:
            return {"skipped": "not_found"}
        if _reads_groone_network(network):
            return {"skipped": "manage_inventory"}
        started = time.monotonic()
        try:
            stored = [_store(services, network, kind, first_day, last_day) for kind in ReportKind]
        except GamError as exc:
            if not exc.permanent:
                raise
            log.warning(
                "métricas da network falharam",
                extra={"network_id": network_id, "error": exc.code},
            )
            return {"error": exc.code}
    publish(services.redis, company_uuid, METRICS_UPDATED, {"network_id": network_id})
    result = {
        "daily_rows": stored[0].daily_rows,
        "key_value_rows": stored[1].key_value_rows,
        "rows_without_site": stored[0].rows_without_site,
        "skipped_rows": stored[0].skipped_rows + stored[1].skipped_rows,
        "ms": round((time.monotonic() - started) * 1000),
    }
    log.info(
        "métricas da network gravadas",
        extra={"network_id": network_id, "start": start, "end": end, **result},
    )
    return result


def _network_busy(
    company_id: str, network_id: str, start: str, end: str, attempt: int
) -> dict[str, Any]:
    """A network está ocupada: o lote volta para a fila, até o limite de tentativas."""
    extra = {"network_id": network_id, "start": start, "end": end, "attempt": attempt}
    if attempt >= MAX_LOCK_ATTEMPTS:
        log.warning("métricas da network desistiram: trava ocupada demais", extra=extra)
        return {"skipped": "locked"}
    log.info("métricas da network adiadas: trava ocupada", extra=extra)
    _try_later(company_id, network_id, start, end, attempt + 1)
    return {"skipped": "locked", "attempt": attempt + 1}


def _try_later(company_id: str, network_id: str, start: str, end: str, attempt: int) -> None:
    """Põe o lote de volta na fila daqui a um minuto."""
    sync_metrics.apply_async(
        args=(company_id, network_id, start, end, attempt), countdown=LOCK_RETRY_SECONDS
    )


@app.task(name="avant.gam.backfill_metrics")
def backfill_metrics(company_id: str, network_id: str, days: int = BACKFILL_DAYS) -> int:
    """Encadeia o histórico da network em lotes, um depois do outro; devolve quantos lotes."""
    today = get_services().clock.now().date()
    periods: list[tuple[date, date]] = []
    chunk_end = today - timedelta(days=1)
    first_day = today - timedelta(days=days)
    while chunk_end >= first_day:
        chunk_start = max(first_day, chunk_end - timedelta(days=BACKFILL_CHUNK_DAYS - 1))
        periods.append((chunk_start, chunk_end))
        chunk_end = chunk_start - timedelta(days=1)
    if periods:
        _chunks_chain(company_id, network_id, periods).apply_async()
    return len(periods)


def _chunks_chain(company_id: str, network_id: str, periods: list[tuple[date, date]]) -> chain:
    """Os lotes do histórico encadeados, para não disputarem a trava da network entre si."""
    return chain(
        *[
            sync_metrics.si(company_id, network_id, start.isoformat(), end.isoformat())
            for start, end in periods
        ]
    )


@app.task(name="avant.gam.schedule_metrics")
def schedule_metrics() -> int:
    """trusted_uow: ontem e hoje de cada network ativa de todas as Empresas."""
    today = get_services().clock.now().date()
    return _fan_out(today - timedelta(days=1), today)


@app.task(name="avant.gam.schedule_reprocess")
def schedule_reprocess() -> int:
    """trusted_uow: os três dias antes de ontem de cada network ativa."""
    today = get_services().clock.now().date()
    return _fan_out(today - timedelta(days=REPROCESS_DAYS + 1), today - timedelta(days=2))


def _fan_out(start: date, end: date) -> int:
    """Agenda ``sync_metrics`` do período para cada network ativa e devolve quantas."""
    networks = sync_service.active_networks(get_services().trusted_uow())
    for company_id, network_id in networks:
        sync_metrics.delay(str(company_id), str(network_id), start.isoformat(), end.isoformat())
    return len(networks)


def _network(services: Services, company_id: uuid.UUID, network_id: uuid.UUID) -> Network | None:
    """A network pela Empresa dela; some se foi removida depois de enfileirar."""
    with services.uow(company_id) as uow:
        return uow.networks.get(network_id)


def _reads_groone_network(network: Network) -> bool:
    """MCM Manage Inventory: o inventário e os relatórios ficam na network da Groone."""
    return (
        network.connection_type is ConnectionType.MCM
        and network.delegation is Delegation.MANAGE_INVENTORY
    )


def _store(
    services: Services, network: Network, kind: ReportKind, start: date, end: date
) -> StoredMetrics:
    """Baixa um relatório e grava as linhas com o caso de uso do avant-core."""
    rows = services.reports.report(network.network_code, kind, start, end)
    return store_gam_report(
        services.uow(network.company_id), network_id=network.id, rows=rows, clock=services.clock
    )
