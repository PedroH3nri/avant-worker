from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from avant_core.access.models import Role
from avant_core.commissions.enums import CommissionEvent, CommissionStatus
from avant_core.commissions.models import CommissionRule, CommissionWindow
from avant_core.company.models import ClientProfile, Company, Membership
from avant_core.gam.contracts.models import Contract
from avant_core.identity.models import User
from avant_core.metrics.models import GamCounts, GamDailyMetric

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.commissions import (
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


def test_today_is_calculated_and_the_month_closes(services: Services) -> None:
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
                services.clock.now(),
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
                    date=today,
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
    assert calculate_today_commissions.delay().get() == {"assigned": 1, "saved": 1}
    with services.trusted_uow() as uow:
        (window,) = uow.commission_windows.for_company(client.id)
        daily = uow.daily_commissions.get(window.id, today)
        assert daily is not None and (daily.base_micros, daily.commission_micros) == (
            100_000_000,
            10_000_000,
        )
    month = today.strftime("%Y-%m")
    result = close_commissions.delay(month).get()
    assert result["windows"] == 1
    with services.trusted_uow() as uow:
        daily = uow.daily_commissions.get(window.id, today)
        assert daily is not None and daily.status is CommissionStatus.VALIDATED
    assert transfer_clients.delay().get() == {"moved": 0}
