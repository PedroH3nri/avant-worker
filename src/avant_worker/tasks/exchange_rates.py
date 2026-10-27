"""Tarefa das cotações (fila ``default``): o dólar e as outras moedas do painel, por dia.

``sync_exchange_rates`` roda a cada 6 horas (o plano grátis tem 1.000 pedidos por mês).
Grava o fim de cada dia fechado que falta (até ``BACKFILL_DAYS`` para trás na primeira vez)
e a cotação de agora para hoje. Usa ``trusted_uow``: a cotação é dado público, sem
Empresa. Worker sem ``OPENEXCHANGERATES_APP_ID`` não faz nada.
"""

import logging
from datetime import UTC, date, timedelta

from avant_core.money.service import last_rates_day, store_exchange_rates

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.exchange_rates")

BACKFILL_DAYS = 100


@app.task(name="avant.default.sync_exchange_rates")
def sync_exchange_rates() -> dict[str, int | str]:
    """trusted_uow: grava os dias fechados que faltam e a cotação de agora para hoje."""
    services = get_services()
    source = services.exchange_rates
    if source is None:
        log.info("cotações sem OPENEXCHANGERATES_APP_ID: nada gravado")
        return {"skipped": "not_configured"}
    today = services.clock.now().astimezone(UTC).date()
    days = closed_days_to_fetch(last_rates_day(services.trusted_uow()), today)
    for day in days:
        store_exchange_rates(
            services.trusted_uow(), day=day, rates=source.historical(day), clock=services.clock
        )
    store_exchange_rates(
        services.trusted_uow(), day=today, rates=source.latest(), clock=services.clock
    )
    log.info("cotações gravadas", extra={"closed_days": len(days), "today": today.isoformat()})
    return {"closed_days": len(days)}


def closed_days_to_fetch(last_day: date | None, today: date) -> list[date]:
    """Os dias fechados a buscar até ontem: desde o último gravado, que pode ter ficado com a
    cotação do meio do dia, ou ``BACKFILL_DAYS`` atrás na primeira vez."""
    floor = today - timedelta(days=BACKFILL_DAYS)
    start = floor if last_day is None else max(last_day, floor)
    return [start + timedelta(days=offset) for offset in range((today - start).days)]
