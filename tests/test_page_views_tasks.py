from datetime import date, timedelta
from zoneinfo import ZoneInfo

from avant_core.metrics.models import PageViewCount
from sqlalchemy import text

from avant_worker.app import _route, app
from avant_worker.page_views import parse_documents
from avant_worker.services import Services
from avant_worker.tasks.gam import sync_network
from avant_worker.tasks.page_views import schedule_page_views, sync_page_views
from tests.fake_gam import FakePageViews
from tests.test_gam_tasks import company, count, fake, inventory, network

DAY = date(2026, 11, 1)


def page_views(services: Services) -> FakePageViews:
    source = services.page_views
    assert isinstance(source, FakePageViews)
    return source


def test_parse_documents_reads_the_data_counter() -> None:
    documents = [
        {
            "domain": "acai.com.br",
            "date": "2026-11-01",
            "hour": "09",
            "country": "Brazil",
            "count": 12,
        },
        {"domain": "acai.com.br", "date": "2026-11-01", "hour": "x", "count": 1},
        {"domain": "acai.com.br", "hour": "10", "count": 1},
        {"domain": "acai.com.br", "date": "2026-11-01", "hour": 23},
    ]
    first, last = parse_documents(documents)
    assert first == PageViewCount("acai.com.br", DAY, 9, "Brazil", 12)
    assert (last.hour, last.country, last.page_views) == (23, "", 0)


def test_page_view_tasks_are_registered_on_the_default_queue() -> None:
    app.loader.import_default_modules()
    for name in ("avant.default.sync_page_views", "avant.default.schedule_page_views"):
        assert name in app.tasks and _route(name) == {"queue": "default"}
    assert app.conf.beat_schedule["page-views-sync"]["task"] == "avant.default.schedule_page_views"


def test_sync_page_views_stores_and_replaces_counts(services: Services) -> None:
    owner = company(services)
    connected = network(services, owner)
    inventory(fake(services))
    sync_network.delay(str(owner.id), str(connected.id)).get()
    source = page_views(services)
    source.counts_by_network["123"] = [
        PageViewCount("www.acai.com.br", DAY, 9, "Brazil", 10),
        PageViewCount("outro.com", DAY, 9, "Brazil", 3),
    ]
    result = sync_page_views.delay(
        str(owner.id), str(connected.id), "2026-11-01", "2026-11-01"
    ).get()
    assert result == {"rows": 2, "rows_without_site": 1, "skipped_rows": 0}
    source.counts_by_network["123"][0] = PageViewCount("acai.com.br", DAY, 9, "Brazil", 15)
    sync_page_views.delay(str(owner.id), str(connected.id), "2026-11-01", "2026-11-01").get()
    assert count(services, "metrics.page_views_hourly") == 2
    with services.uow(owner.id) as uow:
        linked = "SELECT page_views FROM metrics.page_views_hourly WHERE site_id IS NOT NULL"
        assert uow.session.execute(text(linked)).scalar_one() == 15


def test_schedule_uses_sao_paulo_dates_and_skips_without_mongo(services: Services) -> None:
    owner = company(services)
    connected = network(services, owner)
    inventory(fake(services))
    sync_network.delay(str(owner.id), str(connected.id)).get()
    assert schedule_page_views.delay().get() == 1
    today = services.clock.now().astimezone(ZoneInfo("America/Sao_Paulo")).date()
    assert page_views(services).calls == [("123", today - timedelta(days=1), today)]

    services._page_views = None
    assert schedule_page_views.delay().get() == 0
    skipped = sync_page_views.delay(str(owner.id), str(connected.id), "2026-11-01", "2026-11-01")
    assert skipped.get() == {"skipped": "not_configured"}
