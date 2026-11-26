"""Aviso do detrator do NPS ao gerente de conta (H3 do HubSpot, decisão 22).

Usa ``trusted_uow()`` (sem RLS): lê as respostas de todas as Empresas clientes e grava o aviso no
sino do gerente na Company Groone. Idempotente: cada resposta fica marcada com ``warned_at`` e só
volta a avisar se a pessoa responder de novo no trimestre.
"""

import logging

from avant_core.nps.services import warn_nps_detractors as warn_detractors

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.nps")


@app.task(name="avant.default.warn_nps_detractors")
def warn_nps_detractors() -> int:
    """trusted_uow: avisa os gerentes dos detratores ainda não avisados e devolve quantos."""
    services = get_services()
    warned = warn_detractors(services.trusted_uow(), clock=services.clock)
    if warned:
        log.info("detratores do NPS avisados", extra={"warned": warned})
    return warned
