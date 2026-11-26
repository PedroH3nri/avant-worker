"""Sincronia do Avant com o HubSpot da Groone (decisão 22).

``sync_hubspot`` roda todo minuto pelo beat e só trabalha quando há sincronia pedida ("Sincronizar
agora") ou quando a de rotina venceu (15 minutos). A mensal (beat diário e "Sincronizar agora")
também manda as métricas e as comissões do mês atual e dos dois anteriores, como o Genius. Usa
``trusted_uow`` porque lê clientes, networks, contratos, sites, métricas e comissões de todas as
Empresas; nada do HubSpot volta para o banco além dos vínculos. Sem ``HUBSPOT_ACCESS_TOKEN`` não
faz nada. O token nunca vai para o log.
"""

import logging
from datetime import timedelta
from typing import Any

from avant_core.hubspot.errors import HubspotError
from avant_core.hubspot.services import (
    claim_hubspot_run,
    fail_hubspot_run,
    load_hubspot_plan,
    push_hubspot_records,
    save_hubspot_run,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.hubspot")

LOCK_SECONDS = 15 * 60
SOFT_LIMIT_SECONDS = 12 * 60
HARD_LIMIT_SECONDS = 13 * 60
MONTHLY_RETRY_SECONDS = 5 * 60
MONTHLY_RETRIES = 6


@app.task(
    name="avant.hubspot.sync",
    bind=True,
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
    max_retries=MONTHLY_RETRIES,
)
def sync_hubspot(self: Any, monthly: bool = False) -> dict[str, int]:
    """Manda para o HubSpot o que mudou e grava os vínculos; a mensal e a pedida também mandam
    métricas e comissões. A mensal espera a outra terminar e tenta de novo."""
    services = get_services()
    gateway = services.hubspot
    if gateway is None:
        return {"skipped": 1}
    with services.lock("hubspot_sync", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            if monthly:
                raise self.retry(countdown=MONTHLY_RETRY_SECONDS)
            return {"skipped": 1}
        now = services.clock.now()
        with services.trusted_uow() as uow:
            run = (
                claim_hubspot_run(uow, now, timedelta(0))
                if monthly
                else claim_hubspot_run(uow, now)
            )
            with_months = run is not None and (monthly or run.requested_by is not None)
            plan = load_hubspot_plan(uow, now.date() if with_months else None) if run else None
            uow.commit()
        if run is None or plan is None:
            return {"skipped": 1}
        try:
            outcomes = push_hubspot_records(plan, gateway, services.hubspot_config)
        except HubspotError as error:
            with services.trusted_uow() as uow:
                fail_hubspot_run(uow, run.id, str(error), services.clock.now())
                uow.commit()
            log.warning("sincronia com o HubSpot falhou", extra={"error": error.code})
            return {"failed": 1}
        with services.trusted_uow() as uow:
            saved = save_hubspot_run(uow, run.id, outcomes, services.clock.now())
            uow.commit()
    changed, failed = (saved.changed, saved.failed) if saved else (0, 0)
    log.info("sincronia com o HubSpot terminada", extra={"changed": changed, "failed": failed})
    return {"changed": changed, "failed": failed}
