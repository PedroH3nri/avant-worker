from datetime import timedelta

from avant_core.access.enums import Visibility
from avant_core.metrics.enums import MetricSource, RelativePeriod
from avant_core.metrics.models import Period, QueryDefinition
from avant_core.metrics.services import encode_query
from avant_core.reports.enums import ChartType
from avant_core.reports.models import SavedReport

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.reports import refresh_report_preview, refresh_report_previews
from tests.test_gam_tasks import company


def test_report_preview_tasks_are_registered_on_the_default_queue() -> None:
    app.loader.import_default_modules()
    for name in ("avant.default.refresh_report_preview", "avant.default.refresh_report_previews"):
        assert name in app.tasks
        assert _route(name) == {"queue": "default"}
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.refresh_report_previews" in schedule


def test_previews_are_refreshed_once_and_again_when_old(services: Services) -> None:
    client = company(services)
    query = QueryDefinition(
        MetricSource.GAM, ("impressions",), Period(RelativePeriod.LAST_30_DAYS), ("date",)
    )
    now = services.clock.now()
    owner = client.owner_user_id
    assert owner is not None
    report = SavedReport(
        company_id=client.id,
        owner_user_id=owner,
        name="Impressões por dia",
        query=encode_query(query),
        chart_type=ChartType.LINE,
        chart_options={},
        visibility=Visibility.COMPANY,
        role_ids=[],
        created_by=owner,
        created_at=now,
        updated_at=now,
    )
    with services.uow(client.id) as uow:
        uow.saved_reports.add(report)
        uow.commit()

    assert refresh_report_preview.delay(str(report.id)).get() == {"refreshed": 1}
    with services.uow(client.id) as uow:
        saved = uow.saved_reports.get(report.id)
        assert saved is not None and saved.preview is not None
        assert saved.preview["dimension"] == "date"
    assert refresh_report_previews.delay().get() == {"stale": 0, "refreshed": 0}
    with services.uow(client.id) as uow:
        saved = uow.saved_reports.get(report.id)
        assert saved is not None and saved.preview_at is not None
        saved.preview_at -= timedelta(hours=2)
        uow.commit()
    assert refresh_report_previews.delay().get() == {"stale": 1, "refreshed": 1}
