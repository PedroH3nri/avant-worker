from datetime import UTC, datetime

import httpx
from avant_core.gam.inventory.models import Site
from avant_core.metrics.models import GamCounts, GamDailyMetric
from avant_core.site_checklists.enums import CheckOutcome
from avant_core.site_checklists.models import FetchedPage
from avant_core.site_checklists.services.checklist_rules import current_month, previous_month

from avant_worker.adapters import HttpPageFetcher
from avant_worker.adapters.page_fetcher import USER_AGENT
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.checklists import open_checklists
from tests.test_gam_tasks import company, network

HOME = (
    "<a href='/'>Início</a><a href='/politica-de-cookies'>Cookies</a>"
    "<a href='/politica-de-privacidade'>Privacidade</a>"
    "<form role='search'><input name='s'></form>"
    "<a href='/2026/10/um-post-sobre-praias/'>Praias</a>"
)
ARTICLE = "<meta name='author' content='Ana'><time datetime='2026-10-01'>1 de outubro</time>"


class FakePageFetcher:
    """Devolve as páginas cadastradas; o resto não responde."""

    def __init__(self, pages: dict[str, FetchedPage]) -> None:
        self.pages = pages

    def fetch(self, url: str) -> FetchedPage | None:
        """A página cadastrada para o endereço."""
        return self.pages.get(url)


def test_checklist_tasks_are_registered() -> None:
    app.loader.import_default_modules()
    assert _route("avant.default.open_checklists") == {"queue": "default"}
    assert "avant.default.check_checklist" in app.tasks
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.open_checklists" in schedule


def test_fetcher_sends_the_avant_user_agent_and_reads_only_text() -> None:
    def reply(request: httpx.Request) -> httpx.Response:
        assert request.headers["user-agent"] == USER_AGENT
        if request.url.path == "/velho":
            return httpx.Response(301, headers={"location": "https://blog.com/novo"})
        if request.url.path == "/novo":
            return httpx.Response(
                200, text="<a href='/'>Início</a>", headers={"content-type": "text/html"}
            )
        if request.url.path == "/logo.png":
            return httpx.Response(200, content=b"\x89PNG", headers={"content-type": "image/png"})
        raise httpx.ConnectError("fora do ar", request=request)

    http = httpx.Client(
        transport=httpx.MockTransport(reply),
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
    )
    fetcher = HttpPageFetcher(http, interval=0)
    page = fetcher.fetch("https://blog.com/velho")
    assert page == FetchedPage("https://blog.com/novo", 200, "<a href='/'>Início</a>")
    image = fetcher.fetch("https://blog.com/logo.png")
    assert image is not None and image.body == ""
    assert fetcher.fetch("https://blog.com/fora") is None


def test_open_checklists_checks_sites_that_earned_last_month(services: Services) -> None:
    client = company(services)
    gam_network = network(services, client)
    site = Site(
        client.id,
        "blog.com",
        network_id=gam_network.id,
        gam_site_id="77",
        synced_at=datetime.now(UTC),
    )
    with services.trusted_uow() as uow:
        uow.sites.add(site)
        uow.commit()
    last_month = previous_month(current_month(services.clock.now()))
    with services.trusted_uow() as uow:
        uow.gam_metrics.upsert_daily(
            [
                GamDailyMetric(
                    company_id=client.id,
                    network_id=gam_network.id,
                    date=last_month.replace(day=10),
                    ad_unit_path="blog-topo",
                    country_code="BR",
                    device="desktop",
                    revenue_micros=5_000_000,
                    counts=GamCounts(impressions=1000),
                    synced_at=datetime.now(UTC),
                    site_id=site.id,
                )
            ]
        )
        uow.commit()
    services._page_fetcher = FakePageFetcher(
        {
            "https://blog.com/": FetchedPage("https://blog.com/", 200, HOME),
            "https://blog.com/2026/10/um-post-sobre-praias/": FetchedPage(
                "https://blog.com/2026/10/um-post-sobre-praias/", 200, ARTICLE
            ),
            "https://blog.com/ads.txt": FetchedPage(
                "https://blog.com/ads.txt", 200, "groone.com, 123, DIRECT\n"
            ),
        }
    )
    assert open_checklists.delay().get() == {"to_check": 1}
    with services.trusted_uow() as uow:
        (checklist,) = uow.site_checklists.for_month(current_month(services.clock.now()))
        assert checklist.checked_at is not None
        items = {item.id: item.name for item in uow.site_checklists.items()}
        outcomes = {
            items[result.item_id]: result.outcome
            for result in uow.site_checklists.results(checklist.id)
        }
    assert outcomes["Políticas de cookies"] is CheckOutcome.OK
    assert outcomes["Buscador"] is CheckOutcome.OK
    assert outcomes["Autor"] is CheckOutcome.OK and outcomes["Data"] is CheckOutcome.OK
    assert outcomes["ads.txt"] is CheckOutcome.OK
    assert outcomes["Contato"] is CheckOutcome.FAILED
    assert open_checklists.delay().get() == {"to_check": 0}
