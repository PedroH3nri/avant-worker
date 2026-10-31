"""Os testes rodam as tarefas no próprio processo (task_always_eager) contra um
PostgreSQL real, com as migrations do avant-core.

AVANT_TEST_MIGRATIONS_URL: papel avant_owner. AVANT_TEST_DATABASE_URL: papel avant_app.
Sem as duas, os testes que precisam de banco são pulados. AVANT_TEST_REDIS_URL liga a trava
por network (sem ele, o teste da trava é pulado). O GAM é sempre o de ``fake_gam.py``.
"""

import os
from collections.abc import Iterator

import pytest
import redis
from alembic import command
from alembic.config import Config
from avant_core.gam.client.models import Gam
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
    "metrics.gam_daily",
    "metrics.gam_key_value_daily",
    "ad_units",
    "sites",
    "network_sync_runs",
    "networks",
    "mcm_candidates",
    "audit_logs",
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
        for key in r.scan_iter("avant:lock:*"):
            r.delete(key)
        r.close()
