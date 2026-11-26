"""Réguas de nutrição (M17, uso 3): de hora em hora avalia as réguas, manda os e-mails da vez
pelo Resend, atualiza a situação dos envios e cria a tarefa do gerente no HubSpot.

Usa ``trusted_uow()`` (sem RLS) porque as réguas varrem os clientes de todas as Empresas.
Idempotente: o core põe cada e-mail na fila uma vez por passagem (índice único), e o envio só
sai da fila depois de gravado; rodar duas vezes não manda de novo. Uma rodada por vez (trava).
"""

import logging

from avant_core.hubspot.errors import HubspotError
from avant_core.hubspot.models import HubspotTaskPlan
from avant_core.hubspot.services import push_hubspot_tasks
from avant_core.nurture.services import (
    deliver_nurture,
    evaluate_nurture,
    nurture_task_drafts,
    refresh_nurture_statuses,
    save_nurture_tasks,
)

from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.nurture")

LOCK_SECONDS = 20 * 60
SOFT_LIMIT_SECONDS = 15 * 60
HARD_LIMIT_SECONDS = 16 * 60


@app.task(
    name="avant.default.run_nurture",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def run_nurture() -> dict[str, int]:
    """trusted_uow: avalia as réguas, manda os e-mails, atualiza as situações e cria as tarefas."""
    services = get_services()
    with services.lock("nurture", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        messages = evaluate_nurture(
            services.trusted_uow(), clock=services.clock, base_url=services.settings.app_base_url
        )
        mailer = services.nurture_mailer
        sent = deliver_nurture(services.trusted_uow(), mailer, messages, clock=services.clock)
        changed = refresh_nurture_statuses(services.trusted_uow(), mailer, clock=services.clock)
        tasks = _create_tasks(services)
    log.info(
        "réguas de nutrição em dia",
        extra={"queued": len(messages), "sent": sent, "statuses": changed, "tasks": tasks},
    )
    return {"queued": len(messages), "sent": sent, "statuses": changed, "tasks": tasks}


def _create_tasks(services: Services) -> int:
    """Cria no HubSpot as tarefas das passagens novas; sem o token, não faz nada."""
    gateway = services.hubspot
    if gateway is None:
        return 0
    drafts = nurture_task_drafts(services.trusted_uow(), clock=services.clock)
    if not drafts:
        return 0
    try:
        outcomes = push_hubspot_tasks(HubspotTaskPlan(to_create=drafts), gateway)
    except HubspotError as error:
        log.warning("tarefas da nutrição no HubSpot falharam", extra={"error": error.code})
        return 0
    return save_nurture_tasks(services.trusted_uow(), outcomes)
