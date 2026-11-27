"""Qualidade do tráfego: a tarefa soma o tráfego do dia por site e abre o alerta de cloaker junto
com a suspeita da C2, sem abrir duas vezes."""

import json
from datetime import date

from avant_worker.services import Services
from avant_worker.tasks.ad_tags import ensure_page_view_partitions_task, flush_page_views
from avant_worker.tasks.site_security import aggregate_site_integrity
from avant_worker.tasks.traffic_quality import evaluate_traffic_quality
from tests.test_ad_tag_tasks import _page, _tag, redis_services  # noqa: F401


def test_traffic_quality_counts_day_and_mirrors_cloaker(redis_services: Services) -> None:  # noqa: F811
    services = redis_services
    ensure_page_view_partitions_task()
    tag, site = _tag(services)
    framed = {"signals": ["frame"], "blocked": True, "fingerprint": "real"}
    items = [_page(tag, site, services) for _ in range(20)]
    items += [_page(tag, site, services, integrity=framed) for _ in range(3)]
    services.redis.rpush("avant:page-views:buffer", *(json.dumps(item) for item in items))
    assert flush_page_views()["stored"] == 23
    assert aggregate_site_integrity()["opened"] == 1
    assert evaluate_traffic_quality() == {"found": 1, "opened": 1, "closed": 0}
    with services.uow(tag.company_id) as uow:
        (day,) = uow.site_traffic.for_site(site.id, date(2000, 1, 1))
        assert day.page_views == 23
        (alert,) = uow.traffic_alerts.open_alerts()
        assert alert.site_id == site.id and alert.signal.value == "cloaker"
    assert evaluate_traffic_quality()["opened"] == 0
