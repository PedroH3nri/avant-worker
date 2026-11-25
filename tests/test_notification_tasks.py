import uuid
from datetime import timedelta

from avant_core.company.models import Company
from avant_core.identity.models import User
from avant_core.notifications.enums import NotificationIcon, NotificationKind
from avant_core.notifications.models import Notification
from sqlalchemy import text

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.notifications import purge_old_notifications


def test_purge_task_is_scheduled_on_the_default_queue() -> None:
    app.loader.import_default_modules()
    schedule = app.conf.beat_schedule["notifications-purge"]
    assert schedule["task"] == "avant.default.purge_old_notifications"


def test_purge_removes_only_notifications_older_than_30_days(services: Services) -> None:
    now = services.clock.now()
    user = User(email=f"{uuid.uuid4()}@x.com", name="Ana")
    company = Company("Blog", None, 3, f"blog-{uuid.uuid4()}")
    with services.trusted_uow() as uow:
        uow.users.add(user)
        uow.companies.add(company)
        uow.notifications.add_many(
            Notification(
                company.id,
                user.id,
                NotificationKind.MANUAL,
                NotificationIcon.BELL,
                now - timedelta(days=days),
                title="Aviso",
                text="Texto",
            )
            for days in (31, 40, 2)
        )
        uow.commit()

    assert purge_old_notifications.delay().get() == 2
    with services.trusted_uow() as uow:
        left = uow.session.execute(
            text("SELECT count(*) FROM notifications WHERE company_id = :company"),
            {"company": company.id},
        ).scalar_one()
    assert left == 1
