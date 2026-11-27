"""Comparativo com a rede (M18, C7, decisão 23): todo dia às 06:30 UTC calcula, por país,
categoria e métrica, a mediana e o corte dos 25% melhores dos sites com 30 dias de dados, só nos
grupos com 5 sites de 3 clientes, e troca o que está gravado em ``benchmark_groups``.

Usa ``trusted_uow()`` (sem RLS): lê as métricas de todas as Empresas, mas só grava agregados, sem
id de site nem de cliente. Idempotente: rodar de novo troca os grupos pelos mesmos.
"""

import logging

from avant_core.benchmark.services import record_benchmark_groups

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.benchmark")


@app.task(name="avant.default.record_benchmark_groups")
def record_benchmark() -> dict[str, int]:
    """trusted_uow: recalcula os grupos do comparativo com a rede."""
    services = get_services()
    groups = record_benchmark_groups(services.trusted_uow(), clock=services.clock)
    log.info("grupos do comparativo gravados", extra={"groups": groups})
    return {"groups": groups}
