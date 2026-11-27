"""Segurança do site: o integrity do buffer vai para as páginas vistas e a tarefa soma os sinais
por site, abre a suspeita de cloaker e não avisa duas vezes."""

import json

from sqlalchemy import text

from avant_worker.services import Services
from avant_worker.tasks.ad_tags import ensure_page_view_partitions_task, flush_page_views
from avant_worker.tasks.site_security import aggregate_site_integrity
from tests.test_ad_tag_tasks import _page, _tag, redis_services  # noqa: F401


def test_integrity_signals_become_a_cloaker_alert(redis_services: Services) -> None:  # noqa: F811
    services = redis_services
    ensure_page_view_partitions_task()
    tag, site = _tag(services)
    clean = {"signals": [], "blocked": False, "fingerprint": "real", "browser": "chrome"}
    framed = {"signals": ["frame", "desconhecido"], "blocked": True, "fingerprint": "real"}
    items = [_page(tag, site, services, integrity=clean) for _ in range(20)]
    items += [_page(tag, site, services, integrity=framed) for _ in range(2)]
    items.append(_page(tag, site, services))
    services.redis.rpush("avant:page-views:buffer", *(json.dumps(item) for item in items))
    assert flush_page_views()["stored"] == 23
    assert aggregate_site_integrity() == {"days": 1, "opened": 1, "closed": 0}
    with services.uow(tag.company_id) as uow:
        row = uow.session.execute(
            text("SELECT page_views, flagged, blocked, signals FROM site_integrity_days")
        ).one()
        assert tuple(row) == (23, 2, 2, {"frame": 2})
        alert = uow.cloaker_alerts.open_for(site.id)
        assert alert is not None and (alert.page_views, alert.flagged) == (23, 2)
    assert aggregate_site_integrity()["opened"] == 0
