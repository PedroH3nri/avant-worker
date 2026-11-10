"""Os testes rodam as tarefas no próprio processo (task_always_eager) contra um
PostgreSQL real, com as migrations do avant-core.

AVANT_TEST_MIGRATIONS_URL: papel avant_owner. AVANT_TEST_DATABASE_URL: papel avant_app.
Sem as duas, os testes que precisam de banco são pulados. AVANT_TEST_REDIS_URL liga a trava
por network (sem ele, o teste da trava é pulado). O GAM é sempre o de ``fake_gam.py``.
"""

import os
from collections.abc import Iterator
from datetime import date

import pytest
import redis
from alembic import command
from alembic.config import Config
from avant_core.db.uow import SqlAlchemyUnitOfWork
from avant_core.gam.client.models import Gam
from avant_core.metrics.models import DateRange
from avant_core.shared.clock import SystemClock
from sqlalchemy import Engine, create_engine, text

from avant_worker.app import app
from avant_worker.services import Services, use_services
from avant_worker.settings import Settings
from tests.fake_gam import (
    FakeEarnings,
    FakeExchangeRates,
    FakeGamClient,
    FakePageViews,
    FakeReports,
)

APP_URL = os.environ.get("AVANT_TEST_DATABASE_URL")
OWNER_URL = os.environ.get("AVANT_TEST_MIGRATIONS_URL")
REDIS_URL = os.environ.get("AVANT_TEST_REDIS_URL")
GROONE_NETWORK = "9999"
TABLES = (
    "gam_key_values",
    "gam_tool_runs",
    "daily_commissions",
    "commission_deductions",
    "commission_adjustments",
    "commission_windows",
    "commission_rules",
    "commission_settings",
    "contracts",
    "company_profiles",
    "memberships",
    "roles WHERE company_id IS NOT NULL",
    "metrics.mcm_earnings",
    "metrics.exchange_rates",
    "metrics.page_views_hourly",
    "metrics.gam_network_daily",
    "metrics.gam_network_daily_detail",
    "metrics.gam_domain_daily",
    "metrics.gam_domain_daily_detail",
    "metrics.gam_ad_unit_daily",
    "metrics.gam_ad_unit_daily_detail",
    "metrics.gam_key_value_daily",
    "metrics.gam_key_value_daily_detail",
    "metrics.page_view_events",
    "metrics.page_views_key_value_hourly",
    "metrics.ad_tag_daily",
    "metrics.gam_key_value_hourly",
    "price_rule_history",
    "price_rule_configs",
    "price_rules",
    "price_rule_blocks",
    "price_rule_settings",
    "ad_tags",
    "ad_units",
    "sites",
    "network_sync_runs",
    "networks",
    "mcm_candidates",
    "audit_logs",
    "alert_events",
    "schedule_deliveries",
    "report_schedules",
    "metric_alerts",
    "saved_report_pins",
    "saved_reports",
    "companies",
    "sessions",
    "password_resets",
    "user_credentials",
    "users",
)


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    if not (APP_URL and OWNER_URL):
        pytest.skip("defina AVANT_TEST_DATABASE_URL e AVANT_TEST_MIGRATIONS_URL")
    cfg = Config()
    cfg.set_main_option("script_location", "avant_core:migrations")
    os.environ["DATABASE_MIGRATIONS_URL"] = OWNER_URL
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    eng = create_engine(APP_URL)
    yield eng
    eng.dispose()


@pytest.fixture
def services(engine: Engine) -> Iterator[Services]:
    r = redis.Redis.from_url(REDIS_URL) if REDIS_URL else None
    s = Services(
        settings=Settings(database_url=APP_URL or "", avant_env="test"),
        engine=engine,
        clock=SystemClock(),
        redis=r,
        gam_override=Gam(FakeGamClient(), GROONE_NETWORK),
        reports_override=FakeReports(),
        page_views_override=FakePageViews(),
        exchange_rates_override=FakeExchangeRates(),
        earnings_override=FakeEarnings(),
    )
    use_services(s)
    app.conf.task_always_eager = True
    yield s
    app.conf.task_always_eager = False
    use_services(None)
    owner = create_engine(OWNER_URL or "")
    with owner.begin() as conn:
        for table in TABLES:
            conn.execute(text(f"DELETE FROM {table}"))
    owner.dispose()
    if r is not None:
        for pattern in ("avant:lock:*", "kv:*", "avant:price-floors:*", "avant:gam:currency:*"):
            for key in r.scan_iter(pattern):
                r.delete(key)
        r.close()


def refresh_levels(uow: SqlAlchemyUnitOfWork) -> None:
    """Regrava os níveis das métricas das networks gravadas direto na base (sem o relatório)."""
    query = "SELECT DISTINCT network_id FROM metrics.gam_ad_unit_daily_detail"
    for network_id in uow.session.execute(text(query)).scalars():
        uow.gam_metrics.refresh_levels(network_id, DateRange(date(2000, 1, 1), date(2100, 1, 1)))
