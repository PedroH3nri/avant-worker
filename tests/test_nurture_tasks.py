import uuid
from datetime import timedelta

from avant_core.company.enums import CompanyStatus
from avant_core.company.models import ClientProfile, Company
from avant_core.identity.models import User
from avant_core.nurture.enums import NurtureComparison, NurtureMeasure, NurtureSendStatus
from avant_core.nurture.models import NurtureEmail, NurtureMessage, NurtureRule
from avant_core.shared.ids import new_id

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.nurture import run_nurture


class FakeNurtureMailer:
    """Guarda os e-mails e responde que foram abertos."""

    def __init__(self) -> None:
        self.sent: list[NurtureMessage] = []

    def send_nurture(self, message: NurtureMessage) -> str | None:
        """Guarda o e-mail."""
        self.sent.append(message)
        return f"re_{len(self.sent)}"

    def nurture_status(self, provider_id: str) -> NurtureSendStatus | None:
        """Todo envio foi aberto."""
        return NurtureSendStatus.OPENED


def test_nurture_runs_every_hour_on_the_default_queue() -> None:
    """A avaliação das réguas roda de hora em hora, na fila default."""
    app.loader.import_default_modules()
    assert app.conf.beat_schedule["nurture-run"]["task"] == "avant.default.run_nurture"


def test_run_sends_each_email_once_and_reads_the_status(services: Services) -> None:
    """O cliente ativo entra na régua, recebe o e-mail uma vez e a abertura é gravada."""
    email = f"dono-{uuid.uuid4()}@blog.com"
    owner = User(email=email, name="Dono")
    client = ClientProfile(new_id(), "Dono", "Blog", email, user_id=owner.id)
    client.name, client.status = "Blog", CompanyStatus.ACTIVE
    company = Company("Blog", owner.id, 3, f"blog-{uuid.uuid4()}", client_id=client.id)
    now = services.clock.now()
    texts = {lang: "Oi {nome}" for lang in ("pt", "en", "es")}
    with services.trusted_uow() as uow:
        uow.users.add(owner)
        uow.client_profiles.add(client)
        uow.companies.add(company)
        uow.nurture_rules.add(
            NurtureRule(
                "Todos",
                1,
                NurtureMeasure.DAYS_WITHOUT_ACCESS,
                NurtureComparison.GTE,
                0,
                now - timedelta(days=1),
                now,
                enabled=True,
                emails=[NurtureEmail(0, texts, texts).as_json()],
            )
        )
        uow.commit()
    mailer = FakeNurtureMailer()
    services._nurture_mailer = mailer
    services._hubspot = None
    first = run_nurture.delay().get()
    assert first["sent"] >= 1 and first["tasks"] == 0
    assert [message.subject for message in mailer.sent if message.to == email] == ["Oi Dono"]
    run_nurture.delay().get()
    assert len([message for message in mailer.sent if message.to == email]) == 1
    with services.trusted_uow() as uow:
        (view,) = uow.nurture_sends.views_for_client(client.id, 5)
        assert view.send.status is NurtureSendStatus.OPENED
