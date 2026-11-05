"""Limpeza diária: sessões e links de nova senha vencidos e o histórico mais velho que a retenção
de cada tabela (decisão 11 do avant-core).

Usa trusted_uow: sessões e links são da pessoa, e as funções que apagam o histórico só rodam na
limpeza confiável (app.bypass_rls).
"""

import logging
from dataclasses import asdict

from avant_core.maintenance import purge_expired as purge

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.maintenance")


@app.task(name="avant.default.purge_expired")
def purge_expired() -> dict[str, int]:
    """Apaga o que passou da retenção e registra quantos de cada tabela."""
    services = get_services()
    result = purge(services.trusted_uow(), clock=services.clock)
    counts: dict[str, int] = asdict(result)
    log.info("limpeza feita", extra=counts)
    return counts
