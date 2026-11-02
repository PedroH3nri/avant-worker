"""Tarefas dos alertas de métrica.

- ``schedule_alerts``: de hora em hora, depois das métricas do GAM, pede a conferência de cada
  Empresa que tem alerta. Usa ``trusted_uow`` só para varrer as Empresas.
- ``check_alerts``: confere os alertas de uma Empresa, grava os disparos (o que aconteceu) e
  pede o envio dos avisos que faltam.
  Empresa cliente com ``uow(company_id)``; a Company Groone com ``trusted_uow``, porque os
  alertas dela somam as Empresas cliente (com o RLS ligado ela não vê nenhuma linha delas).
- ``notify_alerts`` (fila ``mail``): manda os avisos dos disparos ainda sem aviso (como avisar).

Rodar duas vezes não repete nada: o disparo aberto segura a conferência e o disparo já avisado
não sai de novo.
"""

import logging
import uuid

from avant_core.alerts.services import (
    companies_with_alerts,
    evaluate_company_alerts,
    notify_alert_events,
)
from avant_core.db.uow import SqlAlchemyUnitOfWork

from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.alerts")

LOCK_SECONDS = 15 * 60


@app.task(name="avant.default.schedule_alerts")
def schedule_alerts() -> dict[str, int]:
    """trusted_uow: pede a conferência dos alertas de cada Empresa que tem algum."""
    services = get_services()
    company_ids = companies_with_alerts(services.trusted_uow())
    for company_id in company_ids:
        check_alerts.delay(str(company_id))
    log.info("conferência dos alertas pedida", extra={"companies": len(company_ids)})
    return {"companies": len(company_ids)}


@app.task(name="avant.default.check_alerts")
def check_alerts(company_id: str) -> dict[str, int]:
    """Confere os alertas da Empresa, grava os disparos e pede o envio dos avisos."""
    services = get_services()
    target = uuid.UUID(company_id)
    with services.lock(f"alerts:{company_id}", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        run = evaluate_company_alerts(
            _company_uow(services, target), company_id=target, clock=services.clock
        )
    if run.alerts:
        notify_alerts.delay(company_id)
    log.info(
        "alertas conferidos",
        extra={
            "company_id": company_id,
            "alerts": run.alerts,
            "checked": run.checked,
            "fired": run.fired,
            "resolved": run.resolved,
        },
    )
    return {
        "alerts": run.alerts,
        "checked": run.checked,
        "fired": run.fired,
        "resolved": run.resolved,
    }


@app.task(name="avant.mail.notify_alerts")
def notify_alerts(company_id: str) -> dict[str, int]:
    """Manda por e-mail os disparos da Empresa ainda sem aviso."""
    services = get_services()
    target = uuid.UUID(company_id)
    with services.lock(f"alerts-mail:{company_id}", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        sent = notify_alert_events(
            _company_uow(services, target),
            company_id=target,
            mailer=services.mailer,
            clock=services.clock,
        )
    log.info("avisos dos alertas enviados", extra={"company_id": company_id, "sent": sent})
    return {"sent": sent}


def _company_uow(services: Services, company_id: uuid.UUID) -> SqlAlchemyUnitOfWork:
    """O Unit of Work da Empresa; o da Groone vem sem RLS para ler as Empresas cliente."""
    with services.trusted_uow() as uow:
        company = uow.companies.get(company_id)
        internal = company is not None and company.is_internal
    return services.trusted_uow() if internal else services.uow(company_id)
