import io
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from avant_core.company.models import Company
from avant_core.gam.inventory.models import AdUnit, Site
from avant_core.gam.networks.models import Network
from avant_core.gam.tools.models import GamTargetNetwork
from avant_core.metrics.models import GamCounts, GamReportRow
from avant_core.price_rules.catalog import FLOOR_CACHE_KEY
from avant_core.price_rules.enums import PriceRuleModel
from avant_core.price_rules.models import PriceRuleBlock, PriceRuleSettings

from avant_worker.adapters import ReportKind, parse_report, report_query
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.price_rules import (
    create_price_rules,
    maintain_price_rule_partitions,
    run_price_rules,
    schedule_price_rule_hours,
)
from tests.test_gam_tasks import company, count, network
from tests.test_metrics_tasks import reports

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
HASH = "0a1b2c3d4e5f6071"
BLOCK = "Acai_Content3_Mobile_20261028"


class CurrencyWriter:
    """Só a leitura da moeda da network."""

    def target_network(self, network_code: str) -> GamTargetNetwork:
        """A network em reais."""
        return GamTargetNetwork(network_code, "BRL", "root")


def days_ago(days: int) -> date:
    """O dia em São Paulo, ``days`` dias atrás."""
    return datetime.now(SAO_PAULO).date() - timedelta(days=days)


def enabled_site(services: Services, client: Company, net: Network) -> Site:
    """O acai.com.br com a regra ligada e o Content3_Mobile como Automática."""
    site = Site(
        client.id,
        "acai.com.br",
        network_id=net.id,
        gam_site_id="s1",
        synced_at=services.clock.now(),
    )
    now = services.clock.now()
    with services.uow(client.id) as uow:
        uow.sites.add(site)
        uow.ad_units.add(
            AdUnit(client.id, net.id, "u3", BLOCK, now, ad_unit_code=BLOCK, site_id=site.id)
        )
        uow.price_rule_settings.add(
            PriceRuleSettings(client.id, site.id, now, active=True, control_percent=10)
        )
        uow.price_rule_settings.replace_blocks(
            site.id,
            [PriceRuleBlock(client.id, site.id, "Content3_Mobile", PriceRuleModel.AUTOMATIC)],
        )
        uow.commit()
    return site


def hour_row(day: date, hour: int) -> GamReportRow:
    """Uma hora do bloco com 1000 elegíveis e R$ 1,80 de receita."""
    return GamReportRow(
        day,
        f"acai.com.br/{BLOCK}",
        "BR",
        "",
        1_800_000,
        GamCounts(impressions=900, eligible_requests=1000, responses_served=900),
        "u3",
        "content_hash",
        HASH,
        hour,
    )


def test_price_rule_tasks_are_registered() -> None:
    app.loader.import_default_modules()
    assert _route("avant.gam.sync_price_rule_hours")["queue"] == "gam"
    for name in (
        "avant.gam.schedule_price_rule_hours",
        "avant.default.run_price_rules",
        "avant.default.create_price_rules",
        "avant.default.maintain_price_rule_partitions",
    ):
        assert name in app.tasks
    beat = {entry["task"] for entry in app.conf.beat_schedule.values()}
    assert {"avant.default.run_price_rules", "avant.gam.schedule_price_rule_hours"} <= beat


def test_hourly_query_and_parse_keep_only_content_hash() -> None:
    query = report_query(ReportKind.PRICE_RULE_HOURS, days_ago(0), days_ago(0), currency="BRL")
    assert query["dimensions"][:3] == ["DATE", "HOUR", "CUSTOM_CRITERIA"]
    assert query["reportCurrency"] == "BRL"
    content = (
        "Dimension.DATE,Dimension.HOUR,Dimension.CUSTOM_CRITERIA,Dimension.AD_UNIT_ID,"
        "Dimension.COUNTRY_CODE\n"
        f"2026-11-01,7,content_hash={HASH},u3,BR\n"
        "2026-11-01,7,utm_source=fb,u3,BR\n"
    )
    (only,) = parse_report(io.BytesIO(content.encode()), ReportKind.PRICE_RULE_HOURS)
    assert (only.hour, only.custom_value) == (7, HASH)


def test_hours_rules_and_engine_run_in_the_network_currency(services: Services) -> None:
    services._gam_writer = CurrencyWriter()  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    site = enabled_site(services, client, net)
    cache = FLOOR_CACHE_KEY.format(site_id=site.id, content_hash=HASH)
    if services.redis is not None:
        services.redis.set(cache, "{}")
    yesterday = days_ago(1)
    reports(services).rows[("123", ReportKind.PRICE_RULE_HOURS)] = [
        hour_row(yesterday, hour) for hour in range(4)
    ]
    assert schedule_price_rule_hours.delay().get() == 1
    assert reports(services).currencies[-1] == "BRL"
    assert count(services, "metrics.gam_key_value_hourly") == 4
    assert create_price_rules.delay().get() == 1
    assert run_price_rules.delay().get() == 1
    assert count(services, "price_rule_history") == 1
    assert services.redis is None or not services.redis.exists(cache)
    assert maintain_price_rule_partitions.delay().get()["created"] >= 0
