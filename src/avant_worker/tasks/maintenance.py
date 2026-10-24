"""Limpeza diária de sessões e links de nova senha vencidos.

Usa trusted_uow: sessões e links são da pessoa, não de uma Empresa.
"""

import logging

from avant_core.maintenance import purge_expired as purge

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.maintenance")


@app.task(name="avant.default.purge_expired")
def purge_expired() -> dict[str, int]:
    """Apaga sessões e links de nova senha vencidos e registra quantos."""
    services = get_services()
    result = purge(services.trusted_uow(), clock=services.clock)
    counts = {"sessions": result.sessions, "password_resets": result.password_resets}
    log.info("limpeza feita", extra=counts)
    return counts
