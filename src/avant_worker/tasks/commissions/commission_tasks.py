"""Tarefas da comissão da equipe Groone, como o ``EmployeeCommissionSync`` do Genius.

A cada hora calcula o dia de hoje e às 03:00 os dois dias anteriores, em rascunho; antes, entrega
aos responsáveis os prazos que nasceram sem pessoa. Às 03:30 passa os clientes dos prazos que
acabaram para o papel de destino. No dia 15, às 05:00 (depois da leitura do ``Mcm_Earnings``
das 03:10), fecha o mês anterior com a dedução do GAM. Tudo com ``trusted_uow``: a comissão lê
todas as Empresas cliente.
"""

import logging
from datetime import UTC, date, timedelta

from avant_core.commissions.services import (
    assign_pending_windows,
    calculate_day,
    close_month,
    transfer_ended_windows,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.commissions")

LOCK_SECONDS = 1800
RECENT_DAYS = 2


def previous_month(today: date) -> date:
    """O primeiro dia do mês anterior ao de ``today``."""
    return (today.replace(day=1) - timedelta(days=1)).replace(day=1)


def _calculate(days: list[date]) -> dict[str, int]:
    """Entrega os prazos sem pessoa e calcula os dias pedidos, numa transação só."""
    services = get_services()
    with services.lock("commissions", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        uow = services.trusted_uow()
        with uow:
            assigned = assign_pending_windows(uow)
            saved = sum(calculate_day(uow, day=day, clock=services.clock) for day in days)
            uow.commit()
    log.info("comissão calculada", extra={"days": len(days), "assigned": assigned, "saved": saved})
    return {"assigned": assigned, "saved": saved}


def _today() -> date:
    """O dia de hoje em UTC."""
    return get_services().clock.now().astimezone(UTC).date()


@app.task(name="avant.default.calculate_today_commissions")
def calculate_today_commissions() -> dict[str, int]:
    """trusted_uow: a comissão de hoje, a cada hora."""
    return _calculate([_today()])


@app.task(name="avant.default.calculate_recent_commissions")
def calculate_recent_commissions() -> dict[str, int]:
    """trusted_uow: os dois dias anteriores de novo, às 03:00, quando o GAM já fechou o dia."""
    today = _today()
    return _calculate([today - timedelta(days=offset) for offset in range(1, RECENT_DAYS + 1)])


@app.task(name="avant.default.transfer_clients")
def transfer_clients() -> dict[str, int]:
    """trusted_uow: passa os clientes dos prazos que acabaram para o papel de destino."""
    services = get_services()
    uow = services.trusted_uow()
    with uow:
        moved = transfer_ended_windows(uow, today=_today(), now=services.clock.now())
        uow.commit()
    log.info("clientes transferidos", extra={"moved": moved})
    return {"moved": moved}


@app.task(name="avant.default.close_commissions")
def close_commissions(month: str | None = None) -> dict[str, int | str]:
    """trusted_uow: fecha o mês pedido (``AAAA-MM``) ou o anterior, com a dedução do GAM."""
    services = get_services()
    target = date.fromisoformat(f"{month}-01") if month else previous_month(_today())
    with services.lock("commissions", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        uow = services.trusted_uow()
        with uow:
            result = close_month(uow, month=target, clock=services.clock)
            uow.commit()
    log.info(
        "comissão fechada",
        extra={"month": target.isoformat(), "windows": result.windows},
    )
    return {
        "month": target.isoformat(),
        "windows": result.windows,
        "deduction_micros": result.deduction_micros,
    }
