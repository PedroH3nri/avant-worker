"""Funil de ativação (M18, C5, decisão 23): todo dia às 05:45 UTC grava a data de cada etapa por
lead e cliente, com os leads criados no HubSpot nos últimos 180 dias (quando há o token) e o que o
Avant vê de cada cliente (convite do MCM, MCM aceito, ad tag e primeira receita).

Usa ``trusted_uow()`` (sem RLS): varre os clientes, as networks e as métricas de todas as Empresas.
Idempotente: rodar de novo no mesmo dia não muda as datas já gravadas.
"""

import logging

from avant_core.activation.services import record_activation_milestones

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.activation")


@app.task(name="avant.default.record_activation_milestones")
def record_activation() -> dict[str, int | bool]:
    """trusted_uow: grava as datas das etapas do funil de ativação."""
    services = get_services()
    run = record_activation_milestones(
        services.trusted_uow(), gateway=services.hubspot, clock=services.clock
    )
    result: dict[str, int | bool] = {
        "leads": run.leads,
        "clients": run.clients,
        "changed": run.changed,
        "hubspot_failed": run.hubspot_failed,
    }
    if run.hubspot_failed:
        log.warning("HubSpot falhou; o funil gravou só as etapas do Avant", extra=result)
    log.info("funil de ativação gravado", extra=result)
    return result
