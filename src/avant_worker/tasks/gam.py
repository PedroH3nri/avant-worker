"""Tarefas do Google Ad Manager (fila ``gam``).

- ``sync_network``: teste de acesso, sites e ad units de uma network, nessa ordem. A API
  enfileira ao conectar e no "sincronizar agora"; a descoberta do MCM, para cada network
  nova. Com ``test=False`` (agendador de 6 em 6 horas), só importa.
- ``check_access``: só o teste de acesso, todo dia.
- ``discover_mcm``: de hora em hora, lê os child publishers da network da Groone. Para
  cada network nova, também pede o histórico das métricas (``backfill_metrics``).
- ``schedule_*``: o agendador chama e elas espalham uma tarefa por network ativa.

Cada network roda com o Unit of Work da própria Empresa (RLS) e uma trava no Redis, para
o agendador e o "sincronizar agora" não importarem a mesma network ao mesmo tempo. Só a
descoberta e os ``schedule_*`` usam ``trusted_uow``: percorrem todas as Empresas.

Erro temporário do GAM (``GamUnavailable``) volta para a fila em 1, 2, 4 e 8 minutos.
Tudo aqui é idempotente: a importação é upsert pelo id do GAM.
"""

import logging
import uuid
from typing import Any

from avant_core.gam import sync
from avant_core.ports import GamError, GamUnavailable
from celery import Task

from avant_worker.app import app
from avant_worker.events import NETWORK_UPDATED, publish
from avant_worker.services import Services, get_services
from avant_worker.tasks.metrics import backfill_metrics

log = logging.getLogger("avant.worker.gam")

# Uma importação grande (milhares de ad units) leva poucos minutos; a trava cai sozinha
# depois disso se o worker morrer no meio.
LOCK_SECONDS = 30 * 60
# Erro temporário: 1, 2, 4 e 8 minutos (retry_backoff dobra a cada tentativa).
RETRY_FOR = (GamUnavailable,)


@app.task(
    name="avant.gam.sync_network",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def sync_network(company_id: str, network_id: str, test: bool = True) -> dict[str, Any]:
    """Testa a network e importa sites e ad units, avisando o painel a cada etapa."""
    services = get_services()
    company_uuid, network_uuid = uuid.UUID(company_id), uuid.UUID(network_id)
    with services.lock(f"gam:network:{network_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            log.info("network já em sincronização", extra={"network_id": network_id})
            return {"skipped": "locked"}
        result: dict[str, Any] = {}
        gam, clock, mailer = services.gam, services.clock, services.mailer
        try:
            if test:
                check = sync.check_network(
                    services.uow(company_uuid),
                    network_id=network_uuid,
                    gam=gam,
                    clock=clock,
                    mailer=mailer,
                )
                _updated(services, company_uuid, network_uuid)
                result["test"] = {"ok": check.ok, "status": check.status.value}
                if not check.ok:
                    log.info(
                        "teste da network falhou",
                        extra={"network_id": network_id, "error": check.error},
                    )
                    return result
            result["sites"] = sync.import_sites(
                services.uow(company_uuid),
                network_id=network_uuid,
                gam=gam,
                clock=clock,
                mailer=mailer,
            )
            _updated(services, company_uuid, network_uuid)
            result["ad_units"] = sync.import_ad_units(
                services.uow(company_uuid),
                network_id=network_uuid,
                gam=gam,
                clock=clock,
                mailer=mailer,
            )
            _updated(services, company_uuid, network_uuid)
        except GamError as exc:
            # A etapa ficou registrada como falha.
            _updated(services, company_uuid, network_uuid)
            if not exc.permanent:
                # Volta para a fila (autoretry).
                raise
            # Já ficou registrado na network e na NetworkSyncRun; não adianta tentar de novo.
            log.warning(
                "importação da network falhou",
                extra={"network_id": network_id, "error": exc.code},
            )
            result["error"] = exc.code
            return result
    log.info("network sincronizada", extra={"network_id": network_id, **_flat(result)})
    return result


@app.task(
    name="avant.gam.check_access",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def check_access(company_id: str, network_id: str) -> dict[str, Any]:
    """Só testa se a conta de serviço ainda lê a network."""
    services = get_services()
    with services.lock(f"gam:network:{network_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": "locked"}
        company_uuid, network_uuid = uuid.UUID(company_id), uuid.UUID(network_id)
        try:
            check = sync.check_network(
                services.uow(company_uuid),
                network_id=network_uuid,
                gam=services.gam,
                clock=services.clock,
                mailer=services.mailer,
            )
        finally:
            _updated(services, company_uuid, network_uuid)
    return {"ok": check.ok, "status": check.status.value, "error": check.error}


@app.task(
    name="avant.gam.discover_mcm",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def discover_mcm() -> dict[str, int]:
    """trusted_uow: a descoberta liga networks a Empresas pelo e-mail do dono."""
    services = get_services()
    with services.lock("gam:discover_mcm", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": 1}
        found = sync.discover_mcm(
            services.trusted_uow(), gam=services.gam, clock=services.clock, mailer=services.mailer
        )
    for company_id, network_id in found.created:
        sync_network.delay(str(company_id), str(network_id))
        backfill_metrics.delay(str(company_id), str(network_id))
    counts = {
        "created": len(found.created),
        "candidates": found.candidates,
        "disconnected": found.disconnected,
        "updated": found.updated,
    }
    log.info("descoberta do MCM", extra=counts)
    return counts


@app.task(name="avant.gam.schedule_tests")
def schedule_tests() -> int:
    """trusted_uow: lista as networks ativas de todas as Empresas."""
    return _fan_out(check_access, {})


@app.task(name="avant.gam.schedule_imports")
def schedule_imports() -> int:
    """trusted_uow: lista as networks ativas de todas as Empresas."""
    return _fan_out(sync_network, {"test": False})


def _fan_out(task: "Task[Any, Any]", kwargs: dict[str, Any]) -> int:
    """Agenda a tarefa para cada network ativa e devolve quantas."""
    networks = sync.active_networks(get_services().trusted_uow())
    for company_id, network_id in networks:
        task.delay(str(company_id), str(network_id), **kwargs)
    return len(networks)


def _updated(services: Services, company_id: uuid.UUID, network_id: uuid.UUID) -> None:
    """Avisa o painel, pelo Redis, que a network mudou."""
    publish(services.redis, company_id, NETWORK_UPDATED, {"network_id": str(network_id)})


def _flat(result: dict[str, Any]) -> dict[str, Any]:
    """Contagens para o log JSON: ``sites_created``, ``ad_units_without_site``..."""
    out: dict[str, Any] = {}
    for step, value in result.items():
        if isinstance(value, dict):
            out.update({f"{step}_{key}": value for key, value in value.items()})
        else:
            out[step] = value
    return out
