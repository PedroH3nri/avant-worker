"""Saúde da carteira (M18, C1, decisão 23): a nota diária de cada cliente e o aviso de queda de
receita ao gerente.

Usa ``trusted_uow()`` (sem RLS): lê os sinais de todos os clientes e grava as tabelas internas e
o aviso no sino do gerente na Company Groone. Idempotente: rodar de novo no mesmo dia troca as
notas do dia, e uma queda aberta não avisa outra vez.
"""

import logging

from avant_core.portfolio_health.services import compute_portfolio_health as compute_health

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.portfolio_health")


@app.task(name="avant.default.compute_portfolio_health")
def compute_portfolio_health() -> dict[str, int]:
    """trusted_uow: grava as notas do dia, abre e fecha as quedas e avisa os gerentes."""
    services = get_services()
    run = compute_health(services.trusted_uow(), clock=services.clock)
    log.info(
        "saúde da carteira calculada",
        extra={"scored": run.scored, "warned": run.warned, "recovered": run.recovered},
    )
    return {"scored": run.scored, "warned": run.warned, "recovered": run.recovered}
