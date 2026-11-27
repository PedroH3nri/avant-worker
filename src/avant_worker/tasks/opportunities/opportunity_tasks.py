"""Oportunidades de receita (M18, C4, decisão 23): todo dia às 06:00 UTC roda as seis regras com
os dados do GAM, da ad tag, da regra de preço, do reward e do ads.txt até ontem, abre ou atualiza
as oportunidades, marca como feitas as que a regra deixou de achar e mede o ganho real das feitas
há 14 dias.

Usa ``trusted_uow()`` (sem RLS): varre os sites e as métricas de todas as Empresas.
Idempotente: rodar de novo no mesmo dia só atualiza as mesmas oportunidades.
"""

import logging

from avant_core.opportunities.services import evaluate_opportunities

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.opportunities")


@app.task(name="avant.default.evaluate_opportunities")
def evaluate_site_opportunities() -> dict[str, int]:
    """trusted_uow: roda as regras de oportunidade e grava o resultado."""
    services = get_services()
    run = evaluate_opportunities(services.trusted_uow(), clock=services.clock)
    result = {
        "found": run.found,
        "opened": run.opened,
        "done": run.done,
        "measured": run.measured,
    }
    log.info("oportunidades avaliadas", extra=result)
    return result
