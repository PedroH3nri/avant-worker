"""Limpeza das notificações do sino (fila ``default``).

``purge_old_notifications`` roda uma vez por dia e apaga, em lotes, as notificações com mais
de 30 dias. Usa ``trusted_uow``: a limpeza passa por todas as Empresas de uma vez, sem ler o
conteúdo de nenhuma.
"""

import logging

from avant_core.notifications.services import purge_notifications
from avant_core.notifications.services.notification_service import PURGE_BATCH

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.notifications")

MAX_BATCHES = 50


@app.task(name="avant.default.purge_old_notifications")
def purge_old_notifications() -> int:
    """trusted_uow: apaga as notificações velhas em lotes até não sobrar nenhuma (ou o teto de
    lotes) e devolve quantas."""
    services = get_services()
    removed = 0
    for _batch in range(MAX_BATCHES):
        count = purge_notifications(services.trusted_uow(), clock=services.clock)
        removed += count
        if count < PURGE_BATCH:
            break
    log.info("notificações antigas apagadas", extra={"removed": removed})
    return removed
