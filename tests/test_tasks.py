import uuid
from datetime import timedelta
from typing import Any

import pytest
from avant_core.identity.models import Session, User
from avant_core.mail import ResendMailer, SmtpMailer
from pydantic import ValidationError
from sqlalchemy import text

from avant_worker.app import QUEUES, _route, app, check_settings
from avant_worker.services import REDIS_TIMEOUT_SECONDS, Services, _mailer, _redis_client
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


MAIL_VARIABLES = ("MAIL_TRANSPORT", "RESEND_API_KEY", "SMTP_URL", "REDIS_URL")
BASE: dict[str, Any] = {"database_url": "postgresql://x", "redis_url": "redis://r"}
RESEND: dict[str, Any] = {**BASE, "mail_transport": "resend", "resend_api_key": "re_x"}
SMTP: dict[str, Any] = {
    **BASE,
    "mail_transport": "smtp",
    "smtp_url": "smtps://avant:senha@smtp.exemplo.com",
}


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    """Tira do ambiente as variáveis de e-mail e do Redis, para cada teste dizer as suas."""
    for name in MAIL_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def _stopped_names(monkeypatch: pytest.MonkeyPatch, env: dict[str, str]) -> str:
    """Sobe a checagem com o ambiente dado e devolve a mensagem do ``SystemExit``."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://avant_app:segredo-do-banco@db/avant")
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    with pytest.raises(SystemExit) as stopped:
        check_settings()
    message = str(stopped.value)
    assert "segredo" not in message
    return message


def test_the_worker_starts_with_resend(clean_env: pytest.MonkeyPatch) -> None:
    assert isinstance(_mailer(Settings(**RESEND)), ResendMailer)


def test_the_worker_starts_with_smtp(clean_env: pytest.MonkeyPatch) -> None:
    assert isinstance(_mailer(Settings(**SMTP)), SmtpMailer)


def test_the_transport_has_no_default(clean_env: pytest.MonkeyPatch) -> None:
    message = _stopped_names(clean_env, {"REDIS_URL": "redis://r"})
    assert message.endswith(": MAIL_TRANSPORT")


@pytest.mark.parametrize(
    ("transport", "needed"), [("resend", "RESEND_API_KEY"), ("smtp", "SMTP_URL")]
)
def test_each_transport_needs_its_own_configuration(
    clean_env: pytest.MonkeyPatch, transport: str, needed: str
) -> None:
    message = _stopped_names(clean_env, {"REDIS_URL": "redis://r", "MAIL_TRANSPORT": transport})
    assert message.endswith(f": {needed}")


def test_an_unknown_transport_does_not_start(clean_env: pytest.MonkeyPatch) -> None:
    message = _stopped_names(clean_env, {"REDIS_URL": "redis://r", "MAIL_TRANSPORT": "sendgrid"})
    assert message.endswith(": MAIL_TRANSPORT")


def test_a_broken_smtp_url_does_not_start_and_hides_the_password(
    clean_env: pytest.MonkeyPatch,
) -> None:
    env = {
        "REDIS_URL": "redis://r",
        "MAIL_TRANSPORT": "smtp",
        "SMTP_URL": "http://avant:segredo-smtp@smtp.exemplo.com",
    }
    message = _stopped_names(clean_env, env)
    assert "SMTP_URL" in message and "segredo-smtp" not in message


@pytest.mark.parametrize(
    "smtp_url",
    [
        "http://avant:segredo-smtp@smtp.exemplo.com",
        "smtps://avant:segredo-smtp@smtp.exemplo.com:porta",
        "smtps://avant:segredo-smtp-çã@smtp.exemplo.com",
    ],
)
def test_an_invalid_smtp_url_fails_in_the_settings_showing_only_the_name(
    clean_env: pytest.MonkeyPatch, smtp_url: str
) -> None:
    with pytest.raises(ValidationError) as error:
        Settings(**{**SMTP, "smtp_url": smtp_url})
    shown = str(error.value) + repr(error.value.errors(include_input=False))
    assert "segredo-smtp" not in shown
    env = {"REDIS_URL": "redis://r", "MAIL_TRANSPORT": "smtp", "SMTP_URL": smtp_url}
    message = _stopped_names(clean_env, env)
    assert message.endswith(": SMTP_URL") and "segredo-smtp" not in message


def test_the_worker_does_not_start_without_redis_and_shows_only_names(
    clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    message = _stopped_names(clean_env, {"MAIL_TRANSPORT": "resend", "RESEND_API_KEY": "re_x"})
    logged = "".join(str(record.__dict__) for record in caplog.records)
    assert message.endswith(": REDIS_URL")
    assert "REDIS_URL" in logged and "segredo" not in logged and "re_x" not in logged


@pytest.mark.parametrize(
    ("values", "field"),
    [
        (RESEND, "redis_url"),
        (RESEND, "resend_api_key"),
        (RESEND, "database_url"),
        (RESEND, "mail_transport"),
        (SMTP, "smtp_url"),
    ],
)
def test_an_empty_variable_does_not_start(
    clean_env: pytest.MonkeyPatch, values: dict[str, Any], field: str
) -> None:
    with pytest.raises(ValidationError):
        Settings(**{**values, field: ""})


def test_a_resend_key_with_only_spaces_does_not_start(clean_env: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValidationError):
        Settings(**{**RESEND, "resend_api_key": "   "})


def test_the_redis_url_needs_a_redis_scheme(clean_env: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValidationError):
        Settings(**{**RESEND, "redis_url": "http://r"})
    Settings(**{**RESEND, "redis_url": "rediss://r"})


def test_the_redis_client_has_short_socket_timeouts(clean_env: pytest.MonkeyPatch) -> None:
    options = _redis_client(Settings(**RESEND)).connection_pool.connection_kwargs
    assert 0 < options["socket_timeout"] <= REDIS_TIMEOUT_SECONDS
    assert 0 < options["socket_connect_timeout"] <= REDIS_TIMEOUT_SECONDS
