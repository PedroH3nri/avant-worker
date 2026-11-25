"""Sincronia do Avant com o HubSpot da Groone (decisão 22).

``sync_hubspot`` roda todo minuto pelo beat e só trabalha quando há sincronia pedida ("Sincronizar
agora") ou quando a de rotina venceu (15 minutos). Usa ``trusted_uow`` porque lê clientes,
networks e contratos de todas as Empresas; nada do HubSpot volta para o banco além dos
vínculos. Sem ``HUBSPOT_ACCESS_TOKEN`` não faz nada. O token nunca vai para o log.
"""

import logging

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


@app.task(
    name="avant.hubspot.sync",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def sync_hubspot() -> dict[str, int]:
    """Manda para o HubSpot o que mudou em clientes, networks e contratos e grava os vínculos."""
    services = get_services()
    gateway = services.hubspot
    if gateway is None:
        return {"skipped": 1}
    with services.lock("hubspot_sync", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        now = services.clock.now()
        with services.trusted_uow() as uow:
            run = claim_hubspot_run(uow, now)
            plan = load_hubspot_plan(uow) if run is not None else None
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
