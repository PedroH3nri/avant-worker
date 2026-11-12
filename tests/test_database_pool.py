"""Pool de conexões do core v0.99.0 no worker: prazos, conta das conexões, fork e papel do
banco na subida (worker#171)."""

from types import SimpleNamespace

import pytest
from avant_core.db.connection_budget import ServiceConnections, check_connection_budget
from celery import signals
from sqlalchemy import Engine, text

from avant_worker import services as services_module
from avant_worker.app import check_database_role
from avant_worker.services import Services, use_services
from avant_worker.settings import Settings
from tests.conftest import APP_URL, OWNER_URL

VM_MAX_CONNECTIONS = 200
VM_RESERVED = 10
WORKER_PROCESSES = 4
WORKER_GAM_PROCESSES = 2


def _settings(database_url: str = "postgresql+psycopg://avant_app:app@localhost/avant") -> Settings:
    """As settings padrão do worker, com as variáveis obrigatórias preenchidas."""
    return Settings(database_url=database_url, redis_url="redis://r", resend_api_key="re_x")


def test_default_engine_settings_are_valid_and_named() -> None:
    engine_settings = _settings().engine_settings()
    assert engine_settings.application_name == "avant-worker"
    assert engine_settings.idle_in_transaction_timeout_ms > 0


def test_the_default_pool_fits_the_connection_budget() -> None:
    settings = _settings()
    pools = [
        ServiceConnections(name, processes, settings.db_pool_size, settings.db_max_overflow)
        for name, processes in (("worker", WORKER_PROCESSES), ("worker-gam", WORKER_GAM_PROCESSES))
    ]
    total = check_connection_budget(pools, max_connections=VM_MAX_CONNECTIONS, reserved=VM_RESERVED)
    assert total == (WORKER_PROCESSES + WORKER_GAM_PROCESSES) * settings.db_pool_size


class FakeEngine:
    """Engine que só registra como foi descartado."""

    def __init__(self) -> None:
        self.disposed: list[bool] = []

    def dispose(self, close: bool = True) -> None:
        """Registra o descarte."""
        self.disposed.append(close)


def test_each_forked_child_gets_a_new_pool_without_closing_the_parent() -> None:
    engine = FakeEngine()
    use_services(SimpleNamespace(engine=engine))  # type: ignore[arg-type]
    try:
        signals.worker_process_init.send(sender=None)
        assert engine.disposed == [False]
        assert services_module._current is None
    finally:
        use_services(None)


def test_the_connection_carries_the_worker_name_and_timeouts(services: Services) -> None:
    with services.engine.connect() as connection:
        name = connection.execute(text("SHOW application_name")).scalar_one()
        idle = connection.execute(text("SHOW idle_in_transaction_session_timeout")).scalar_one()
    assert name == "avant-worker"
    assert idle == "5min"


def test_the_app_role_passes_the_start_check(engine: Engine) -> None:
    check_database_role(_settings(APP_URL or ""))


def test_an_owner_role_does_not_start_and_the_password_stays_out(engine: Engine) -> None:
    with pytest.raises(SystemExit) as stopped:
        check_database_role(_settings(OWNER_URL or ""))
    assert "RLS" in str(stopped.value)
    assert "owner@" not in str(stopped.value)


def test_an_unreachable_database_does_not_start() -> None:
    url = "postgresql+psycopg://avant_app:segredo-do-banco@localhost:1/avant"
    with pytest.raises(SystemExit) as stopped:
        check_database_role(_settings(url))
    assert "segredo-do-banco" not in str(stopped.value)
