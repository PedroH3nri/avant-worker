import json
from datetime import UTC, datetime

from avant_core.ad_tags.models import AdTag, AdTagDraft, AdTagSettings, AdTagVersion
from avant_core.ad_tags.services import draft_to_json
from avant_core.company.models import Company
from avant_core.gam.inventory.models import Site
from avant_core.install_checks.enums import InstallCheckSource, InstallCheckState, InstallTarget
from avant_core.loaders.models import Loader
from avant_core.rewards.models import Reward
from avant_core.site_checklists.models import FetchedPage

from avant_worker.adapters import channel
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.install_checks import check_install, daily_install_checks
from tests.test_gam_tasks import company

TAG_LINE = '<script async src="https://avant.groone.com/tag.js" data-tag="tg_abcd1234"></script>'
HOME = f"<html><head>{TAG_LINE}</head><body></body></html>"


class CountingFetcher:
    """Devolve as páginas cadastradas e conta as buscas; o resto não responde."""

    def __init__(self, pages: dict[str, FetchedPage]) -> None:
        self.pages = pages
        self.calls: list[str] = []

    def fetch(self, url: str) -> FetchedPage | None:
        """A página cadastrada para o endereço."""
        self.calls.append(url)
        return self.pages.get(url)


def _seed(services: Services) -> tuple[Company, AdTag, Loader, Reward]:
    """Um cliente com blog.com, uma ad tag publicada com loader e reward e um reward ativo."""
    client = company(services)
    now = datetime(2026, 11, 24, 6, tzinfo=UTC)
    site = Site(client.id, "blog.com")
    loader = Loader(client.id, "Padrão", None, now, now)
    draft = draft_to_json(AdTagDraft((), AdTagSettings(reward=True, loader_id=loader.id)))
    tag = AdTag(client.id, site.id, "Principal", "tg_abcd1234", None, now, now, draft)
    version = AdTagVersion(client.id, tag.id, 1, draft, loader.id, None, now)
    tag.loader_id = loader.id
    reward = Reward(client.id, site.id, "Prêmio", "/premio", "T", "D", "B", None, now, now)
    reward.icon_emoji = "🎁"
    with services.uow(client.id) as uow:
        uow.sites.add(site)
        uow.loaders.add(loader)
        uow.ad_tags.add(tag)
        uow.ad_tag_versions.add(version)
        tag.published_version_id = version.id
        uow.rewards.add(reward)
        uow.commit()
    return client, tag, loader, reward


def test_install_tasks_are_registered() -> None:
    app.loader.import_default_modules()
    assert _route("avant.default.check_install") == {"queue": "default"}
    assert "avant.default.check_site_installs" in app.tasks
    schedule = {item["task"] for item in app.conf.beat_schedule.values()}
    assert "avant.default.daily_install_checks" in schedule


def test_check_install_saves_and_tells_the_screen(services: Services) -> None:
    client, tag, _loader, _reward = _seed(services)
    services._page_fetcher = CountingFetcher(
        {"https://blog.com/": FetchedPage("https://blog.com/", 200, HOME)}
    )
    pubsub = services.redis.pubsub()  # type: ignore[no-untyped-call]
    pubsub.subscribe(channel(client.id))
    pubsub.get_message(timeout=1)
    result = check_install.delay(str(client.id), "ad_tag", str(tag.id)).get()
    assert result == {"checked": 1}
    message = pubsub.get_message(timeout=1)
    pubsub.close()
    assert message is not None
    assert json.loads(message["data"]) == {
        "type": "install_check.updated",
        "data": {"target": "ad_tag", "target_id": str(tag.id)},
    }
    with services.uow(client.id) as uow:
        check = uow.install_checks.get(InstallTarget.AD_TAG, tag.id)
        assert check is not None and check.state is InstallCheckState.DONE
        assert {finding.code for finding in check.finding_list()} >= {"tag_found"}


def test_daily_checks_fetch_each_page_once(services: Services) -> None:
    client, tag, loader, reward = _seed(services)
    fetcher = CountingFetcher(
        {
            "https://blog.com/": FetchedPage("https://blog.com/", 200, HOME),
            "https://blog.com/premio": FetchedPage("https://blog.com/premio", 200, HOME),
        }
    )
    services._page_fetcher = fetcher
    assert daily_install_checks.delay().get() == {"sites": 1, "items": 4}
    assert fetcher.calls.count("https://blog.com/") == 1
    with services.uow(client.id) as uow:
        checks = [
            uow.install_checks.get(InstallTarget.AD_TAG, tag.id),
            uow.install_checks.get(InstallTarget.LOADER, loader.id),
            uow.install_checks.get(InstallTarget.REWARD, reward.id),
            uow.install_checks.get(InstallTarget.SECURITY, tag.site_id),
        ]
        assert all(check is not None for check in checks)
        assert {check.source for check in checks if check} == {InstallCheckSource.DAILY}
        reward_check = checks[2]
        assert reward_check is not None
        assert {finding.code for finding in reward_check.finding_list()} == {"reward_in_tag"}
