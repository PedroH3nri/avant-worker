"""Qualidade do tráfego (M18, C3, decisão 23): soma o tráfego de hoje e de ontem por site, roda as
regras de tráfego inválido (CTR, sessões que saem em segundos, pico de páginas vistas, dedução do
MCM e suspeita de cloaker) e abre, atualiza ou fecha os alertas.

Usa ``trusted_uow()`` (sem RLS): varre as páginas vistas e as métricas de todas as Empresas.
Idempotente: regrava hoje e ontem, e um alerta aberto só é atualizado.
"""

import logging

from avant_core.traffic_quality.services import evaluate_traffic

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.traffic_quality")


@app.task(name="avant.default.evaluate_traffic_quality")
def evaluate_traffic_quality() -> dict[str, int]:
    """trusted_uow: roda as regras de tráfego e grava os alertas."""
    services = get_services()
    run = evaluate_traffic(services.trusted_uow(), clock=services.clock)
    log.info(
        "qualidade do tráfego avaliada",
        extra={"found": run.found, "opened": run.opened, "closed": run.closed},
    )
    return {"found": run.found, "opened": run.opened, "closed": run.closed}
