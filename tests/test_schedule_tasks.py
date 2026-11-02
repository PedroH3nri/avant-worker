from datetime import timedelta

from avant_core.access.enums import Visibility
from avant_core.company.models import Membership
from avant_core.metrics.enums import MetricSource, RelativePeriod
from avant_core.metrics.models import Period, QueryDefinition
from avant_core.metrics.services import encode_query
from avant_core.reports.enums import ChartType
from avant_core.reports.models import SavedReport
from avant_core.schedules.enums import ScheduleFrequency, ScheduleTarget
from avant_core.schedules.models import ReportSchedule

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.schedules import deliver_reports, schedule_reports
from tests.test_alert_tasks import RecordingMailer
from tests.test_gam_tasks import company


def test_schedule_tasks_are_registered_on_their_queues() -> None:
    app.loader.import_default_modules()
    assert _route("avant.default.schedule_reports") == {"queue": "default"}
    assert _route("avant.mail.deliver_reports") == {"queue": "mail"}
    for name in ("avant.default.schedule_reports", "avant.mail.deliver_reports"):
        assert name in app.tasks
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.schedule_reports" in schedule


def test_due_reports_go_out_once(services: Services) -> None:
    client = company(services)
    owner = client.owner_user_id
    assert owner is not None
    now = services.clock.now()
    query = QueryDefinition(MetricSource.GAM, ("impressions",), Period(RelativePeriod.YESTERDAY))
    report = SavedReport(
        company_id=client.id,
        owner_user_id=owner,
        name="Impressões",
        query=encode_query(query),
        chart_type=ChartType.TABLE,
        chart_options={},
        visibility=Visibility.COMPANY,
        role_ids=[],
        created_by=owner,
        created_at=now,
        updated_at=now,
    )
    schedule = ReportSchedule(
        company_id=client.id,
        owner_user_id=owner,
        name="Resumo diário",
        target=ScheduleTarget.REPORT,
        report_id=report.id,
        frequency=ScheduleFrequency.DAILY,
        hour=9,
        timezone="America/Sao_Paulo",
        recipient_user_ids=[owner],
        next_run_at=now - timedelta(minutes=2),
        created_by=owner,
        created_at=now,
        updated_at=now,
    )
    with services.uow(client.id) as uow:
        uow.memberships.add(Membership(client.id, owner, None, now))
        uow.saved_reports.add(report)
        uow.report_schedules.add(schedule)
        uow.commit()
    mailer = RecordingMailer()
    services.mailer = mailer

    assert schedule_reports.delay().get() == {"companies": 1}
    assert [to for to, _ in mailer.reports] == ["dono@acai.com.br"]
    assert mailer.reports[0][1].title == "Impressões"
    assert mailer.reports[0][1].attachment_name.endswith(".csv")
    again = deliver_reports.delay(str(client.id)).get()
    assert again == {"due": 0, "sent": 0, "emails": 0}
    assert len(mailer.reports) == 1
