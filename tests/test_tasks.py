import uuid
from datetime import timedelta

from avant_core.identity.domain import Session, User
from sqlalchemy import text

from avant_worker.app import QUEUES, _route, app
from avant_worker.services import Services
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
    assert result == {"sessions": 1, "password_resets": 0}
    with services.engine.connect() as conn:
        left = conn.execute(text("SELECT count(*) FROM sessions")).scalar_one()
    assert left == 1
