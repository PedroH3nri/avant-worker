import uuid

from avant_core.company.models import ClientProfile, Company
from avant_core.identity.models import User
from avant_core.nps.models import NpsResponse
from avant_core.nps.services import quarter_of
from sqlalchemy import text

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.nps import warn_nps_detractors


def test_warn_task_is_scheduled_on_the_default_queue() -> None:
    """A tarefa roda a cada 5 minutos na fila default."""
    app.loader.import_default_modules()
    schedule = app.conf.beat_schedule["nps-detractors"]
    assert schedule["task"] == "avant.default.warn_nps_detractors"


def test_detractor_reaches_the_manager_once(services: Services) -> None:
    """A nota baixa vira aviso no sino do gerente na Groone, uma vez só."""
    now = services.clock.now()
    manager = User(email=f"{uuid.uuid4()}@groone.com", name="Gerente")
    person = User(email=f"{uuid.uuid4()}@blog.com", name="Dona")
    with services.trusted_uow() as uow:
        uow.users.add(manager)
        uow.users.add(person)
        groone = uow.companies.internal()
        if groone is None:
            groone = Company("Groone", manager.id, None, f"groone-{uuid.uuid4()}", is_internal=True)
            uow.companies.add(groone)
        company = Company("Blog", None, 3, f"blog-{uuid.uuid4()}")
        client = ClientProfile(company.id, "Dona", "Blog", person.email)
        client.account_manager_id = manager.id
        uow.client_profiles.add(client)
        company.client_id = client.id
        uow.companies.add(company)
        response = NpsResponse(company.id, person.id, quarter_of(now.date()), now)
        response.score = 2
        uow.nps_responses.add(response)
        uow.commit()

    assert warn_nps_detractors.delay().get() >= 1
    assert warn_nps_detractors.delay().get() == 0
    with services.trusted_uow() as uow:
        notices = uow.session.execute(
            text("SELECT count(*) FROM notifications WHERE user_id = :manager AND kind = :kind"),
            {"manager": manager.id, "kind": "nps_detractor"},
        ).scalar_one()
    assert notices == 1
