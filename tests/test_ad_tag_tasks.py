"""Ad tag: o buffer das páginas vistas vira visitas e saúde, as partições e o cache depois da
importação."""

import json
import uuid
from datetime import timedelta

import pytest
from avant_core.ad_tags.models import AdTag
from avant_core.gam.inventory.models import Site
from sqlalchemy import text

from avant_worker.services import Services
from avant_worker.tasks.ad_tags import (
    ensure_page_view_partitions_task,
    flush_page_views,
    forget_network_ad_tags,
)
from tests.test_gam_tasks import company, network


class FakeCountries:
    """Um IP conhecido no Brasil; o resto não está na base."""

    def __init__(self) -> None:
        self.asked: list[str | None] = []

    def country(self, ip: str | None) -> str | None:
        """Brazil para 200.1.1.1."""
        self.asked.append(ip)
        return "Brazil" if ip == "200.1.1.1" else None


@pytest.fixture
def redis_services(services: Services) -> Services:
    """Os serviços com Redis e o país pelo IP falso."""
    if services.redis is None:
        pytest.skip("defina AVANT_TEST_REDIS_URL")
    services._countries = FakeCountries()
    return services


def _tag(services: Services) -> tuple[AdTag, Site]:
    """Um site com network e uma ad tag."""
    owner = company(services, email=f"dono-{uuid.uuid4().hex[:6]}@blog.com")
    found = network(services, owner, code=uuid.uuid4().hex[:8])
    domain = f"blog-{uuid.uuid4().hex[:6]}.com"
    site = Site(owner.id, domain, network_id=found.id, gam_site_id=uuid.uuid4().hex[:10])
    now = services.clock.now()
    tag = AdTag(owner.id, site.id, "Principal", f"tg_{uuid.uuid4().hex[:8]}", None, now, now)
    with services.uow(owner.id) as uow:
        uow.sites.add(site)
        uow.ad_tags.add(tag)
        uow.commit()
    return tag, site


def _page(tag: AdTag, site: Site, services: Services, **changes: object) -> dict[str, object]:
    """O JSON de uma página vista como a api guarda."""
    page: dict[str, object] = {
        "key": tag.key,
        "url": f"https://{site.domain}/receitas/bolo?utm_source=google",
        "page_view_id": str(uuid.uuid4()),
        "visitor_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "version": 1,
        "device": "mobile",
        "language": "pt-BR",
        "referrer": None,
        "visible_ms": 5000,
        "scroll_percent": 80,
        "clicked": False,
        "adblock": False,
        "id_post": "42",
        "content_hash": None,
        "blocks": [{"type": "Content3", "state": "rendered"}, {"type": "Anchor", "state": "empty"}],
        "ip": "200.1.1.1",
        "received_at": services.clock.now().isoformat(),
    }
    page.update(changes)
    return page


def test_buffer_becomes_page_views_and_health(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    ensure_page_view_partitions_task()
    tag, site = _tag(services)
    first = _page(tag, site, services)
    items = [first, _page(tag, site, services, ip="10.0.0.1"), _page(tag, site, services, key="x")]
    services.redis.rpush("avant:page-views:buffer", *(json.dumps(item) for item in items), "{ru")
    services.redis.rpush("avant:page-views:processing:sobra", json.dumps(first))
    totals = flush_page_views()
    assert totals == {"stored": 2, "duplicates": 1, "skipped": 2, "without_network": 0}
    assert not services.redis.exists("avant:page-views:buffer")
    assert list(services.redis.scan_iter("avant:page-views:processing:*")) == []
    with services.uow(tag.company_id) as uow:
        countries = uow.session.execute(
            text(
                "SELECT country, sum(page_views) FROM metrics.page_views_hourly"
                " WHERE domain = :domain GROUP BY country ORDER BY country"
            ),
            {"domain": site.domain},
        ).all()
        assert [tuple(row) for row in countries] == [("Brazil", 1), ("unknown", 1)]
        seen = uow.ad_tag_health.last_seen([tag.id])
        assert seen[tag.id].version == 1
    assert flush_page_views() == {"stored": 0, "duplicates": 0, "skipped": 0, "without_network": 0}


def test_partitions_are_created_once(redis_services: Services) -> None:
    services = redis_services
    ensure_page_view_partitions_task()
    assert ensure_page_view_partitions_task() == 0
    tomorrow = (services.clock.now() + timedelta(days=1)).strftime("%Y%m%d")
    with services.trusted_uow() as uow:
        found = uow.session.execute(
            text("SELECT to_regclass(:name) IS NOT NULL"),
            {"name": f"metrics.page_view_events_{tomorrow}"},
        ).scalar_one()
    assert found


def test_import_forgets_the_network_tags(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    tag, site = _tag(services)
    assert site.network_id is not None
    key = f"avant:tag:{tag.key}"
    services.redis.set(key, "{}")
    assert forget_network_ad_tags(services, site.network_id) == 1
    assert not services.redis.exists(key)
