from dataclasses import dataclass, field

from avant_core.alerts.models import AlertMail, MetricAlert
from avant_core.company.enums import InvitationKind
from avant_core.company.models import Membership
from avant_core.metrics.enums import MetricSource, RelativePeriod
from avant_core.metrics.models import Period, QueryDefinition
from avant_core.metrics.services import encode_query
from avant_core.ports import Notice

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.alerts import check_alerts, schedule_alerts
from tests.test_gam_tasks import company


@dataclass
class RecordingMailer:
    """Guarda os avisos dos alertas que sairiam."""

    alerts: list[tuple[str, AlertMail]] = field(default_factory=list)

    def send_invitation(
        self, *, to: str, token: str, kind: InvitationKind, company_name: str | None, locale: str
    ) -> None:
        """Não usado aqui."""

    def send_password_reset(self, *, to: str, token: str, locale: str) -> None:
        """Não usado aqui."""

    def send_notice(
        self, *, to: str, notice: Notice, locale: str, params: dict[str, str] | None = None
    ) -> None:
        """Não usado aqui."""

    def send_metric_alert(self, *, to: str, locale: str, alert: AlertMail) -> None:
        """Guarda o aviso do alerta."""
        self.alerts.append((to, alert))


def test_alert_tasks_are_registered_on_their_queues() -> None:
    app.loader.import_default_modules()
    assert _route("avant.default.schedule_alerts") == {"queue": "default"}
    assert _route("avant.default.check_alerts") == {"queue": "default"}
    assert _route("avant.mail.notify_alerts") == {"queue": "mail"}
    for name in (
        "avant.default.schedule_alerts",
        "avant.default.check_alerts",
        "avant.mail.notify_alerts",
    ):
        assert name in app.tasks
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.schedule_alerts" in schedule


def test_alerts_fire_once_and_mail_the_list_once(services: Services) -> None:
    client = company(services)
    owner = client.owner_user_id
    assert owner is not None
    now = services.clock.now()
    query = QueryDefinition(MetricSource.GAM, ("impressions",), Period(RelativePeriod.YESTERDAY))
    alert = MetricAlert(
        company_id=client.id,
        owner_user_id=owner,
        name="Sem impressões",
        definition={
            "schema_version": 1,
            "query": encode_query(query),
            "condition": "below",
            "value": "1",
            "baseline": None,
        },
        recipient_user_ids=[owner],
        currency="USD",
        created_by=owner,
        created_at=now,
        updated_at=now,
    )
    with services.uow(client.id) as uow:
        uow.memberships.add(Membership(client.id, owner, None, now))
        uow.metric_alerts.add(alert)
        uow.commit()
    mailer = RecordingMailer()
    services.mailer = mailer

    assert schedule_alerts.delay().get() == {"companies": 1}
    assert [to for to, _ in mailer.alerts] == ["dono@acai.com.br"]
    assert mailer.alerts[0][1].alert_name == "Sem impressões"
    again = check_alerts.delay(str(client.id)).get()
    assert again == {"alerts": 1, "checked": 1, "fired": 0, "resolved": 0}
    assert len(mailer.alerts) == 1
