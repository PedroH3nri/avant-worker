"""Os testes rodam as tarefas no próprio processo (task_always_eager) contra um
PostgreSQL real, com as migrations do avant-core.

AVANT_TEST_MIGRATIONS_URL: papel avant_owner. AVANT_TEST_DATABASE_URL: papel avant_app.
Sem as duas, os testes que precisam de banco são pulados.
"""

import os
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from avant_core.shared.clock import SystemClock
from sqlalchemy import Engine, create_engine, text

from avant_worker.app import app
from avant_worker.services import Services, use_services
from avant_worker.settings import Settings

APP_URL = os.environ.get("AVANT_TEST_DATABASE_URL")
OWNER_URL = os.environ.get("AVANT_TEST_MIGRATIONS_URL")


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
    s = Services(
        settings=Settings(database_url=APP_URL or "", avant_env="test"),
        engine=engine,
        clock=SystemClock(),
    )
    use_services(s)
    app.conf.task_always_eager = True
    yield s
    app.conf.task_always_eager = False
    use_services(None)
    owner = create_engine(OWNER_URL or "")
    with owner.begin() as conn:
        for table in ("sessions", "password_resets", "user_credentials", "users"):
            conn.execute(text(f"DELETE FROM {table}"))
    owner.dispose()
