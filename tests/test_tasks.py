import uuid
from datetime import timedelta

import pytest
from avant_core.identity.models import Session, User
from avant_core.mail import ResendMailer
from pydantic import ValidationError
from sqlalchemy import text

from avant_worker.app import QUEUES, _route, app, check_settings
from avant_worker.services import Services, _mailer
from avant_worker.settings import Settings
from avant_worker.tasks.maintenance import purge_expired


def test_queue_comes_from_the_task_name() -> None:
    assert _route("avant.gam.discover_networks") == {"queue": "gam"}
    assert _route("avant.mail.send") == {"queue": "mail"}
    assert _route("avant.default.purge_expired") == {"queue": "default"}
    assert _route("avant.outra.coisa") == {"queue": "default"}
    assert _route("celery.chord_unlock") == {"queue": "default"}
    assert set(QUEUES) == {"default", "mail", "gam"}


def test_beat_schedule_points_at_registered_tasks() -> None:
    app.loader.import_default_modules()
    for entry in app.conf.beat_schedule.values():
        assert entry["task"] in app.tasks
    assert app.conf.task_acks_late and app.conf.worker_prefetch_multiplier == 1


def test_purge_expired(services: Services) -> None:
    now = services.clock.now()
    user = User(email=f"{uuid.uuid4()}@x.com", name="Ana")
    old = Session(
        user_id=user.id,
        token_hash=str(uuid.uuid4()),
        created_at=now - timedelta(days=70),
        last_seen_at=now - timedelta(days=65),
        expires_at=now - timedelta(days=40),
    )
    live = Session(
        user_id=user.id,
        token_hash=str(uuid.uuid4()),
        created_at=now,
        last_seen_at=now,
        expires_at=now + timedelta(days=7),
    )
    with services.trusted_uow() as uow:
        uow.users.add(user)
        uow.sessions.add(old)
        uow.sessions.add(live)
        uow.commit()

    result = purge_expired.delay().get()
    assert result["sessions"] == 1 and result["password_resets"] == 0
    assert set(result) >= {"audit_logs", "sync_runs", "gam_tool_runs"}
    with services.engine.connect() as conn:
        left = conn.execute(text("SELECT count(*) FROM sessions")).scalar_one()
    assert left == 1


@pytest.mark.parametrize("env", ["local", "test", "staging", "production"])
def test_every_env_needs_redis_and_resend(env: str) -> None:
    with pytest.raises(ValidationError) as error:
        Settings(database_url="postgresql://x", avant_env=env, _env_file=None)
    missing = {str(item["loc"][0]) for item in error.value.errors()}
    assert missing == {"redis_url", "resend_api_key"}
    Settings(
        database_url="postgresql://x",
        avant_env=env,
        redis_url="redis://r",
        resend_api_key="re_x",
    )


def test_the_worker_does_not_start_without_redis_or_resend(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://avant_app:segredo-do-banco@db/avant")
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    with pytest.raises(SystemExit) as stopped:
        check_settings()
    logged = [str(record.__dict__) for record in caplog.records]
    assert "REDIS_URL, RESEND_API_KEY" in str(stopped.value)
    assert any("REDIS_URL, RESEND_API_KEY" in record for record in logged)
    assert "segredo-do-banco" not in str(stopped.value) + "".join(logged)


def test_the_worker_mailer_is_always_resend() -> None:
    settings = Settings(
        database_url="postgresql://x",
        avant_env="local",
        redis_url="redis://r",
        resend_api_key="re_x",
    )
    assert isinstance(_mailer(settings), ResendMailer)
