"""Tarefas da comissão da equipe Groone, como o ``EmployeeCommissionSync`` do Genius.

A cada hora calcula o dia de hoje e às 03:00 todos os dias ainda em aberto, em rascunho; antes,
entrega aos responsáveis os prazos que nasceram sem pessoa. Às 03:30 passa os clientes dos prazos
que acabaram para o papel de destino. Do dia 15 ao 20, às 05:00 (depois da leitura do
``Mcm_Earnings`` das 03:10), fecha o mês anterior com a dedução do GAM, só quando o
``Mcm_Earnings`` do mês já chegou; fechar de novo não muda nada. Tudo com ``trusted_uow``: a
comissão lê todas as Empresas cliente.
"""

import logging
from datetime import UTC, date, timedelta

from avant_core.commissions.services import (
    assign_pending_windows,
    calculate_day,
    close_month,
    open_days,
    transfer_ended_windows,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.commissions")

LOCK_SECONDS = 3600
LAST_CLOSING_DAY = 20


def previous_month(today: date) -> date:
    """O primeiro dia do mês anterior ao de ``today``."""
    return (today.replace(day=1) - timedelta(days=1)).replace(day=1)


def _calculate(day: date | None) -> dict[str, int]:
    """Entrega os prazos sem pessoa e calcula o dia pedido, ou todos os dias em aberto até ontem,
    numa transação só."""
    services = get_services()
    with services.lock("commissions", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        uow = services.trusted_uow()
        with uow:
            assigned = assign_pending_windows(uow)
            days = [day] if day is not None else open_days(uow, today=_today())
            saved = sum(calculate_day(uow, day=item, clock=services.clock) for item in days)
            uow.commit()
    log.info("comissão calculada", extra={"days": len(days), "assigned": assigned, "saved": saved})
    return {"assigned": assigned, "saved": saved}


def _today() -> date:
    """O dia de hoje em UTC."""
    return get_services().clock.now().astimezone(UTC).date()


@app.task(name="avant.default.calculate_today_commissions")
def calculate_today_commissions() -> dict[str, int]:
    """trusted_uow: a comissão de hoje, a cada hora."""
    return _calculate(_today())


@app.task(name="avant.default.calculate_recent_commissions")
def calculate_recent_commissions() -> dict[str, int]:
    """trusted_uow: todos os dias ainda em aberto até ontem, às 03:00, quando o GAM já fechou o
    dia; paga desde o início os prazos entregues tarde."""
    return _calculate(None)


@app.task(name="avant.default.transfer_clients")
def transfer_clients() -> dict[str, int]:
    """trusted_uow: passa os clientes dos prazos que acabaram para o papel de destino."""
    services = get_services()
    with services.lock("commissions", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        uow = services.trusted_uow()
        with uow:
            moved = transfer_ended_windows(uow, today=_today(), now=services.clock.now())
            uow.commit()
    log.info("clientes transferidos", extra={"moved": moved})
    return {"moved": moved}


@app.task(name="avant.default.close_commissions")
def close_commissions(month: str | None = None) -> dict[str, int | str]:
    """trusted_uow: fecha o mês pedido (``AAAA-MM``) ou o anterior, com a dedução do GAM; espera o
    ``Mcm_Earnings`` do mês chegar."""
    services = get_services()
    today = _today()
    target = date.fromisoformat(f"{month}-01") if month else previous_month(today)
    with services.lock("commissions", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            _warn_if_late(today, target, "trava ocupada")
            return {"skipped": 1}
        uow = services.trusted_uow()
        with uow:
            arrived = uow.mcm_earnings.last_month()
            if arrived is None or arrived < target:
                _warn_if_late(today, target, "Mcm_Earnings do mês ainda não chegou")
                return {"month": target.isoformat(), "waiting": 1}
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


def _warn_if_late(today: date, target: date, reason: str) -> None:
    """No último dia de fechamento, avisa que o mês ainda não fechou."""
    if today.day >= LAST_CLOSING_DAY:
        log.error(
            "comissão do mês não fechou", extra={"month": target.isoformat(), "reason": reason}
        )
