"""Tarefas do gerente de conta no HubSpot a partir dos avisos do Avant (decisão 22, H2).

``sync_hubspot_followups`` roda a cada 15 minutos pelo beat: acha os problemas dos clientes
(network com erro ou desconectada, instalação com erro, alerta disparado e detrator), cria uma
tarefa no contato do cliente com o gerente como dono, vê quais o gerente já fez e fecha as dos
problemas que sumiram. Usa ``trusted_uow`` porque varre os clientes de todas as Empresas; uma
tarefa aberta por problema (índice único no core), então rodar duas vezes não duplica. Sem
``HUBSPOT_ACCESS_TOKEN`` não faz nada.
"""

import logging

from avant_core.hubspot.errors import HubspotError
from avant_core.hubspot.services import (
    load_hubspot_tasks,
    push_hubspot_tasks,
    save_hubspot_tasks,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.hubspot")

LOCK_SECONDS = 10 * 60
SOFT_LIMIT_SECONDS = 8 * 60
HARD_LIMIT_SECONDS = 9 * 60


@app.task(
    name="avant.hubspot.followups",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def sync_hubspot_followups() -> dict[str, int]:
    """Cria as tarefas dos problemas novos, marca as feitas e fecha as resolvidas."""
    services = get_services()
    gateway = services.hubspot
    if gateway is None:
        return {"skipped": 1}
    with services.lock("hubspot_followups", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        with services.trusted_uow() as uow:
            plan = load_hubspot_tasks(uow, services.clock.now())
        try:
            outcomes = push_hubspot_tasks(plan, gateway)
        except HubspotError as error:
            log.warning("tarefas do HubSpot falharam", extra={"error": error.code})
            return {"failed": 1}
        with services.trusted_uow() as uow:
            created = save_hubspot_tasks(uow, outcomes, services.clock.now())
    closed = sum(1 for outcome in outcomes if outcome.completed)
    log.info(
        "tarefas do HubSpot em dia", extra={"tasks_created": created, "tasks_completed": closed}
    )
    return {"created": created, "completed": closed}
