import logging
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest
from avant_core.access.models import Role
from avant_core.commissions.enums import CommissionEvent, CommissionStatus
from avant_core.commissions.models import CommissionRule, CommissionWindow
from avant_core.company.models import ClientProfile, Company, Membership
from avant_core.gam.contracts.models import Contract
from avant_core.identity.models import User
from avant_core.metrics.models import GamCounts, GamDailyMetric, McmEarning

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.commissions import (
    calculate_recent_commissions,
    calculate_today_commissions,
    close_commissions,
    previous_month,
    transfer_clients,
)
from tests.test_gam_tasks import company, network


def test_commission_tasks_are_registered_on_the_default_queue() -> None:
    app.loader.import_default_modules()
    for name in (
        "avant.default.calculate_today_commissions",
        "avant.default.calculate_recent_commissions",
        "avant.default.transfer_clients",
        "avant.default.close_commissions",
    ):
        assert name in app.tasks
        assert _route(name) == {"queue": "default"}
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.close_commissions" in schedule


def test_previous_month() -> None:
    assert previous_month(date(2026, 11, 15)) == date(2026, 10, 1)
    assert previous_month(date(2026, 1, 15)) == date(2025, 12, 1)


def seller_scenario(services: Services, revenue_day_offset: int = 0) -> tuple[Company, date]:
    """Um comercial a 10% com o prazo de cadastro de um cliente (revshare de 50%) e US$ 200 de
    receita no dia; devolve o cliente e o dia da receita."""
    today = services.clock.now().astimezone(UTC).date()
    seller = User(email="lucas@groone.com", name="Lucas")
    groone = Company(
        name="Groone", owner_user_id=None, seat_limit=None, slug="groone-teste", is_internal=True
    )
    client = company(services)
    n = network(services, client)
    with services.trusted_uow() as uow:
        uow.users.add(seller)
        groone.owner_user_id = seller.id
        uow.companies.add(groone)
        role = Role(key="externo", name={"pt": "Externo"}, company_id=groone.id)
        uow.roles.add(role)
        uow.memberships.add(Membership(groone.id, seller.id, role.id, services.clock.now()))
        uow.commission_rules.add(
            CommissionRule(
                role.id,
                CommissionEvent.CLIENT_CREATED,
                Decimal("10"),
                0,
                None,
                None,
                services.clock.now() - timedelta(days=60),
            )
        )
        uow.client_profiles.add(
            ClientProfile(client.id, "Dono", "Açaí", "dono@acai.com", account_manager_id=seller.id)
        )
        uow.contracts.add(
            Contract(client.id, n.id, Decimal("50"), datetime(2026, 1, 1, tzinfo=UTC))
        )
        uow.commission_windows.add(
            CommissionWindow(
                CommissionEvent.CLIENT_CREATED,
                client.id,
                today - timedelta(days=40),
                services.clock.now(),
            )
        )
        uow.commission_settings.set(today - timedelta(days=40))
        uow.gam_metrics.upsert_daily(
            [
                GamDailyMetric(
                    company_id=client.id,
                    network_id=n.id,
                    date=today - timedelta(days=revenue_day_offset),
                    ad_unit_path="topo",
                    country_code="BR",
                    device="desktop",
                    revenue_micros=200_000_000,
                    counts=GamCounts(impressions=10),
                    synced_at=services.clock.now(),
                )
            ]
        )
        uow.commit()
    return client, today - timedelta(days=revenue_day_offset)


def test_today_is_calculated_and_the_month_closes(services: Services) -> None:
    client, today = seller_scenario(services)
    assert calculate_today_commissions.delay().get() == {"assigned": 1, "saved": 1}
    with services.trusted_uow() as uow:
        (window,) = uow.commission_windows.for_company(client.id)
        daily = uow.daily_commissions.get(window.id, today)
        assert daily is not None and (daily.base_micros, daily.commission_micros) == (
            100_000_000,
            10_000_000,
        )
    assert transfer_clients.delay().get() == {"moved": 0}


def earnings(services: Services, client: Company, month: date) -> None:
    """Grava o Mcm_Earnings do mês da network do cliente."""
    with services.trusted_uow() as uow:
        (n,) = uow.networks.list_for_company(client.id)
        uow.mcm_earnings.upsert(
            [
                McmEarning(
                    company_id=client.id,
                    network_id=n.id,
                    month=month,
                    delegation=None,
                    currency="USD",
                    total_earnings_micros=0,
                    deductions_micros=0,
                    child_payment_micros=0,
                    parent_payment_micros=0,
                    synced_at=services.clock.now(),
                )
            ]
        )
        uow.commit()


def test_the_daily_run_fills_every_open_day(services: Services) -> None:
    client, day = seller_scenario(services, revenue_day_offset=5)
    assert calculate_recent_commissions.delay().get()["saved"] >= 5
    with services.trusted_uow() as uow:
        (window,) = uow.commission_windows.for_company(client.id)
        daily = uow.daily_commissions.get(window.id, day)
        assert daily is not None and daily.commission_micros == 10_000_000


def test_closing_runs_every_day_from_the_15th_to_the_20th() -> None:
    (entry,) = [
        item
        for item in app.conf.beat_schedule.values()
        if item["task"] == "avant.default.close_commissions"
    ]
    assert entry["schedule"].day_of_month == set(range(15, 21))


def test_a_busy_lock_skips_the_run(services: Services) -> None:
    if services.redis is None:
        pytest.skip("sem Redis")
    held = services.redis.lock("avant:lock:commissions", timeout=60, blocking=False)
    assert held.acquire()
    try:
        assert calculate_recent_commissions.delay().get() == {"skipped": 1}
        assert transfer_clients.delay().get() == {"skipped": 1}
    finally:
        held.release()


def test_a_long_run_renews_the_lock(services: Services) -> None:
    if services.redis is None:
        pytest.skip("sem Redis")
    with services.lock("teste-renova", timeout=5) as acquired:
        assert acquired
        services.renew_lock("teste-renova", timeout=300)
        ttl = int(str(services.redis.pttl("avant:lock:teste-renova")))
        assert ttl > 5_000


def test_closing_warns_on_the_20th_when_the_month_is_still_open(
    services: Services, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.ERROR, logger="avant.worker.commissions")
    real = services.clock
    services.clock = FixedClock(datetime(2026, 11, 20, 5, tzinfo=UTC))
    try:
        assert close_commissions.delay().get() == {"month": "2026-10-01", "waiting": 1}
    finally:
        services.clock = real
    assert any("não fechou" in record.message for record in caplog.records)


def test_closing_the_current_month_is_refused(services: Services) -> None:
    client, today = seller_scenario(services)
    earnings(services, client, today.replace(day=1))
    month = today.strftime("%Y-%m")
    assert close_commissions.delay(month).get() == {"month": f"{month}-01", "refused": 1}


class FixedClock:
    """Relógio parado num instante, para os testes de data."""

    def __init__(self, instant: datetime) -> None:
        self.instant = instant

    def now(self) -> datetime:
        return self.instant


def test_last_month_closes_after_its_earnings_arrive(services: Services) -> None:
    today = services.clock.now().astimezone(UTC).date()
    client, day = seller_scenario(services, revenue_day_offset=today.day)
    calculate_recent_commissions.delay().get()
    month = day.strftime("%Y-%m")
    assert close_commissions.delay(month).get() == {"month": f"{month}-01", "waiting": 1}
    earnings(services, client, day.replace(day=1))
    result = close_commissions.delay(month).get()
    assert result["windows"] == 1
    with services.trusted_uow() as uow:
        (window,) = uow.commission_windows.for_company(client.id)
        daily = uow.daily_commissions.get(window.id, day)
        assert daily is not None and daily.status is CommissionStatus.VALIDATED


def test_renewing_a_lost_lock_says_so(services: Services) -> None:
    if services.redis is None:
        pytest.skip("sem Redis")
    with services.lock("teste-perdida", timeout=60) as acquired:
        assert acquired
        services.redis.delete("avant:lock:teste-perdida")
        assert services.renew_lock("teste-perdida", timeout=60) is False
