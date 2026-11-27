"""Oportunidades de receita: a tarefa diária abre a do ads.txt e não abre duas vezes."""

from datetime import timedelta

from avant_core.install_checks.enums import InstallCheckSource, InstallCheckState, InstallTarget
from avant_core.install_checks.models import InstallCheck
from sqlalchemy import text

from avant_worker.services import Services
from avant_worker.tasks.opportunities import evaluate_site_opportunities
from tests.test_ad_tag_tasks import _tag, redis_services  # noqa: F401

METRIC_ROW = """
    INSERT INTO metrics.gam_ad_unit_daily (company_id, network_id, date, parent_ad_unit,
        child_ad_unit, site_id, currency, revenue_micros, impressions, unfilled_impressions,
        viewable_impressions, measurable_impressions, clicks, eligible_requests,
        responses_served, synced_at)
    VALUES (:company, :network, :day, :parent, 'Blog_Content1_Mobile_20261110', :site, 'USD',
        50000000, 10000, 0, 0, 0, 0, 0, 0, now())
"""


def test_opportunities_open_ads_txt_once(redis_services: Services) -> None:  # noqa: F811
    services = redis_services
    tag, site = _tag(services)
    now = services.clock.now()
    with services.trusted_uow() as uow:
        uow.install_checks.add(
            InstallCheck(
                company_id=tag.company_id,
                target=InstallTarget.AD_TAG,
                target_id=tag.id,
                state=InstallCheckState.DONE,
                source=InstallCheckSource.DAILY,
                requested_at=now,
                finished_at=now,
                findings=[{"code": "ads_txt_missing", "severity": "error"}],
            )
        )
        uow.session.execute(
            text(METRIC_ROW),
            {
                "company": tag.company_id,
                "network": site.network_id,
                "day": (now - timedelta(days=3)).date(),
                "parent": site.domain,
                "site": site.id,
            },
        )
        uow.commit()
    assert evaluate_site_opportunities() == {"found": 1, "opened": 1, "done": 0, "measured": 0}
    with services.uow(tag.company_id) as uow:
        (item,) = uow.site_opportunities.open()
        assert item.site_id == site.id and item.gain_micros == 5_000_000
    assert evaluate_site_opportunities()["opened"] == 0
