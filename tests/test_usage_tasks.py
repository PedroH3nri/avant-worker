import uuid

from avant_core.company.models import Company
from avant_core.identity.models import User
from avant_core.usage.models import UsageIncrement
from avant_core.usage.services import usage_day
from sqlalchemy import text

from avant_worker.adapters.usage_counter import RedisUsageCounter
from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.usage import flush_usage, purge_usage


def test_usage_tasks_are_scheduled_on_the_default_queue() -> None:
    """A gravação roda de hora em hora e a limpeza uma vez por dia, na fila default."""
    app.loader.import_default_modules()
    assert app.conf.beat_schedule["usage-flush"]["task"] == "avant.default.flush_usage"
    assert app.conf.beat_schedule["usage-purge"]["task"] == "avant.default.purge_usage"


def test_flush_writes_the_day_totals_once(services: Services) -> None:
    """Os totais do Redis vão para o banco; rodar de novo regrava o mesmo dia."""
    person = User(email=f"{uuid.uuid4()}@blog.com", name="Bia")
    company = Company("Blog", None, 3, f"blog-{uuid.uuid4()}")
    with services.trusted_uow() as uow:
        uow.users.add(person)
        uow.companies.add(company)
        uow.commit()
    for key in services.redis.scan_iter("avant:usage:*"):
        services.redis.delete(key)
    counter = RedisUsageCounter(services.redis)
    day = usage_day(services.clock.now())
    counter.add(UsageIncrement(person.id, company.id, day, sessions=1, screens=2, area="reports"))
    counter.add(UsageIncrement(person.id, company.id, day, active_minutes=3))

    assert flush_usage.delay().get() >= 1
    assert flush_usage.delay().get() >= 1
    with services.trusted_uow() as uow:
        rows = uow.session.execute(
            text(
                "SELECT sessions, screens, active_minutes, areas FROM user_usage_daily"
                " WHERE company_id = :company"
            ),
            {"company": company.id},
        ).all()
    assert [tuple(row) for row in rows] == [(1, 2, 3, {"reports": 1})]
    assert purge_usage.delay().get() == 0
