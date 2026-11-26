"""Uso do Avant por pessoa (M17, uso 2).

Usa ``trusted_uow()`` (sem RLS): grava os totais do dia de todas as Empresas e apaga o uso
antigo de todas. Idempotente: ``flush_usage`` regrava os totais de hoje e de ontem que estão no
Redis (``adapters/usage_counter.py``), então rodar duas vezes grava o mesmo.
"""

import logging

from avant_core.usage.services import flush_usage as flush_usage_days
from avant_core.usage.services import purge_usage as purge_old_usage

from avant_worker.adapters.usage_counter import RedisUsageCounter
from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.usage")


@app.task(name="avant.default.flush_usage", soft_time_limit=8 * 60, time_limit=9 * 60)
def flush_usage() -> int:
    """trusted_uow: grava no banco os totais de uso de hoje e de ontem e devolve quantas linhas."""
    services = get_services()
    saved = flush_usage_days(
        services.trusted_uow(), RedisUsageCounter(services.redis), clock=services.clock
    )
    log.info("uso do painel gravado", extra={"rows": saved})
    return saved


@app.task(name="avant.default.purge_usage")
def purge_usage() -> int:
    """trusted_uow: apaga o uso de mais de 13 meses e devolve quantos dias apagou."""
    services = get_services()
    removed = purge_old_usage(services.trusted_uow(), clock=services.clock)
    if removed:
        log.info("uso antigo apagado", extra={"removed": removed})
    return removed
