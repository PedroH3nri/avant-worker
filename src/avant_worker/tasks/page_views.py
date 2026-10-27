"""Tarefas das visitas (fila ``default``): o contador de page views do iGroone/data.

- ``sync_page_views``: lê no Mongo do data as visitas de uma network num período e grava com
  ``store_page_views`` do avant-core (a contagem de cada hora troca pela mais nova).
- ``schedule_page_views``: de hora em hora, ontem e hoje (datas de São Paulo, como no data)
  de cada network ativa.

Cada network roda com o Unit of Work da própria Empresa (RLS) e uma trava no Redis. Só o
``schedule_page_views`` usa ``trusted_uow``: lista as networks de todas as Empresas. Worker
sem ``PAGE_VIEWS_MONGO_URL`` não agenda nada.
"""

import logging
import uuid
from datetime import date, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from avant_core.gam import sync_service
from avant_core.metrics.service import store_page_views

from avant_worker.app import app
from avant_worker.events import METRICS_UPDATED, publish
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.page_views")

LOCK_SECONDS = 10 * 60
DATA_TIMEZONE = ZoneInfo("America/Sao_Paulo")


@app.task(name="avant.default.sync_page_views")
def sync_page_views(company_id: str, network_id: str, start: str, end: str) -> dict[str, Any]:
    """Grava as visitas da network entre ``start`` e ``end`` (datas ISO, inclusive)."""
    services = get_services()
    source = services.page_views
    if source is None:
        return {"skipped": "not_configured"}
    company_uuid, network_uuid = uuid.UUID(company_id), uuid.UUID(network_id)
    with services.lock(f"page_views:{network_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": "locked"}
        with services.uow(company_uuid) as uow:
            network = uow.networks.get(network_uuid)
        if network is None:
            return {"skipped": "not_found"}
        counts = source.counts(
            network.network_code, date.fromisoformat(start), date.fromisoformat(end)
        )
        stored = store_page_views(
            services.uow(company_uuid), network_id=network_uuid, counts=counts, clock=services.clock
        )
    publish(services.redis, company_uuid, METRICS_UPDATED, {"network_id": network_id})
    result = {
        "rows": stored.rows,
        "rows_without_site": stored.rows_without_site,
        "skipped_rows": stored.skipped_rows,
    }
    log.info(
        "visitas da network gravadas",
        extra={"network_id": network_id, "start": start, "end": end, **result},
    )
    return result


@app.task(name="avant.default.schedule_page_views")
def schedule_page_views() -> int:
    """trusted_uow: ontem e hoje (São Paulo) de cada network ativa; devolve quantas."""
    services = get_services()
    if services.page_views is None:
        log.info("visitas sem PAGE_VIEWS_MONGO_URL: nada agendado")
        return 0
    today = services.clock.now().astimezone(DATA_TIMEZONE).date()
    start, end = (today - timedelta(days=1)).isoformat(), today.isoformat()
    networks = sync_service.active_networks(services.trusted_uow())
    for company_id, network_id in networks:
        sync_page_views.delay(str(company_id), str(network_id), start, end)
    return len(networks)
