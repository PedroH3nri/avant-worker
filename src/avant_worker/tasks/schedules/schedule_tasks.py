"""Tarefas dos envios agendados de relatório e dashboard.

- ``schedule_reports``: de hora em hora (minuto 2, logo depois da hora cheia em que os envios
  saem), pede o envio de cada Empresa com algum envio na hora. Usa ``trusted_uow`` só para
  varrer as Empresas.
- ``deliver_reports`` (fila ``mail``): roda o relatório ou o dashboard como cada pessoa da lista
  e manda o e-mail com o resumo e o CSV anexo. Empresa cliente com ``uow(company_id)``; a
  Company Groone sem RLS, porque os relatórios dela somam as Empresas cliente.

Rodar duas vezes não repete: o horário é marcado como enviado (único por envio e horário) e o
próximo calculado antes de mandar.
"""

import logging
import uuid

from avant_core.schedules.services import companies_with_due_schedules, deliver_due_schedules

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.schedules")

LOCK_SECONDS = 30 * 60


@app.task(name="avant.default.schedule_reports")
def schedule_reports() -> dict[str, int]:
    """trusted_uow: pede o envio de cada Empresa com algum envio agendado na hora."""
    services = get_services()
    company_ids = companies_with_due_schedules(services.trusted_uow(), clock=services.clock)
    for company_id in company_ids:
        deliver_reports.delay(str(company_id))
    log.info("envios agendados pedidos", extra={"companies": len(company_ids)})
    return {"companies": len(company_ids)}


@app.task(name="avant.mail.deliver_reports")
def deliver_reports(company_id: str) -> dict[str, int]:
    """Manda os envios agendados da Empresa cujo horário chegou."""
    services = get_services()
    target = uuid.UUID(company_id)
    with services.lock(f"schedules:{company_id}", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        run = deliver_due_schedules(
            services.report_uow(target),
            company_id=target,
            mailer=services.mailer,
            clock=services.clock,
        )
    log.info(
        "envios agendados enviados",
        extra={"company_id": company_id, "due": run.due, "sent": run.sent, "emails": run.emails},
    )
    return {"due": run.due, "sent": run.sent, "emails": run.emails}
