"""Tarefa dos ganhos e deduções do MCM (fila ``gam``), como o ``PaymentsGamSync`` do Genius.

O GAM fecha o mês por volta do dia 15 do mês seguinte. ``sync_mcm_earnings`` roda do dia 15
ao 20, às 03:10 UTC (00:10 em São Paulo), e regrava o mês anterior: se o GAM corrigir algum
número nesses dias, a última leitura vale. Na primeira vez, busca também os
``BACKFILL_MONTHS`` meses antes. Os ganhos vêm da network da Groone e são de todas as
Empresas, por isso a gravação usa ``trusted_uow``.
"""

import logging
from datetime import UTC, date

from avant_core.metrics.earnings_service import last_earnings_month, store_mcm_earnings

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.earnings")

BACKFILL_MONTHS = 12
LOCK_SECONDS = 1800


@app.task(name="avant.gam.sync_mcm_earnings")
def sync_mcm_earnings(month: str | None = None) -> dict[str, int | str]:
    """trusted_uow: grava os ganhos do mês pedido (``AAAA-MM``) ou dos meses que faltam."""
    services = get_services()
    groone_code = services.settings.gam_groone_network_code
    if not groone_code:
        log.warning("ganhos do MCM sem GAM_GROONE_NETWORK_CODE: nada gravado")
        return {"skipped": "not_configured"}
    with services.lock("mcm-earnings", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": "locked"}
        today = services.clock.now().astimezone(UTC).date()
        if month:
            months = [date.fromisoformat(f"{month}-01")]
        else:
            months = months_to_fetch(last_earnings_month(services.trusted_uow()), today)
        rows = unknown = 0
        for current in months:
            earnings = services.earnings.list_mcm_earnings(groone_code, current)
            stored = store_mcm_earnings(
                services.trusted_uow(), earnings=earnings, clock=services.clock
            )
            rows += stored.rows
            unknown += stored.unknown_networks
            log.info(
                "ganhos do MCM gravados",
                extra={
                    "month": current.isoformat(),
                    "rows": stored.rows,
                    "unknown_networks": stored.unknown_networks,
                    "skipped_rows": stored.skipped_rows,
                },
            )
    return {"months": len(months), "rows": rows, "unknown_networks": unknown}


def months_to_fetch(last_month: date | None, today: date) -> list[date]:
    """O mês anterior a hoje e, sem nada gravado ainda, os ``BACKFILL_MONTHS`` antes dele;
    depois de um tempo parado, os meses que faltam desde o último gravado."""
    previous = _shift(today.replace(day=1), -1)
    start = _shift(previous, -BACKFILL_MONTHS) if last_month is None else min(last_month, previous)
    start = max(start, _shift(previous, -BACKFILL_MONTHS))
    months = []
    current = start
    while current <= previous:
        months.append(current)
        current = _shift(current, 1)
    return months


def _shift(month: date, offset: int) -> date:
    """O primeiro dia do mês ``offset`` meses antes ou depois."""
    index = month.year * 12 + month.month - 1 + offset
    return date(index // 12, index % 12 + 1, 1)
