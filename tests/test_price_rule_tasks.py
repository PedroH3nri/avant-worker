import io
import logging
import uuid
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from avant_core.company.models import Company
from avant_core.gam.inventory.models import AdUnit, Site
from avant_core.gam.networks.models import Network
from avant_core.gam.tools.models import GamTargetNetwork
from avant_core.metrics.models import GamCounts, GamReportRow
from avant_core.price_rules.catalog import CASCADE_CACHE_KEY, FLOOR_CACHE_KEY
from avant_core.price_rules.enums import PriceRuleModel
from avant_core.price_rules.models import PriceRuleBlock, PriceRuleSettings
from avant_core.price_rules.services import run_site_price_rules
from avant_core.shared.errors import NotFound

from avant_worker.adapters import ReportKind, parse_report, report_query
from avant_worker.adapters.gam_writer import GamTargetNetworkWithTimeZone
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.price_rules import (
    create_price_rules,
    maintain_price_rule_partitions,
    price_rule_tasks,
    run_price_rules,
    schedule_price_rule_hours,
)
from tests.test_gam_tasks import company, count, network
from tests.test_metrics_tasks import reports

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
HASH = "0a1b2c3d4e5f6071"
BLOCK = "Acai_Content3_Mobile_20261028"


class CurrencyWriter:
    """Só a leitura da moeda e do fuso da network."""

    def __init__(self, time_zone: str = "America/Sao_Paulo") -> None:
        self.time_zone = time_zone
        self.calls = 0

    def target_network(self, network_code: str) -> GamTargetNetwork:
        """A network em reais, com o fuso configurado."""
        self.calls += 1
        return GamTargetNetworkWithTimeZone(network_code, "BRL", "root", self.time_zone)


class FakeLock:
    """A trava do Redis sempre concedida."""

    def acquire(self) -> bool:
        """Concede a trava."""
        return True

    def release(self) -> None:
        """Solta a trava."""


class FakeRedis:
    """Só o que as tarefas de regra de preço usam do Redis: trava, texto e apagar chaves."""

    def __init__(self) -> None:
        self.values: dict[str, bytes] = {}
        self.deleted: list[str] = []

    def lock(self, *_args: Any, **_kwargs: Any) -> FakeLock:
        """Uma trava sempre concedida."""
        return FakeLock()

    def get(self, key: str) -> bytes | None:
        """O valor guardado, se houver."""
        return self.values.get(key)

    def set(self, key: str, value: str, ex: int | None = None) -> None:
        """Guarda o texto (o prazo não importa aqui)."""
        self.values[key] = value.encode()

    def delete(self, *keys: str) -> None:
        """Anota as chaves apagadas."""
        self.deleted.extend(keys)


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


def hour_row(
    day: date, hour: int, custom_key: str = "content_hash", custom_value: str = HASH
) -> GamReportRow:
    """Uma hora do bloco com 1000 elegíveis e R$ 1,80 de receita."""
    return GamReportRow(
        day,
        f"acai.com.br/{BLOCK}",
        "BR",
        "",
        1_800_000,
        GamCounts(impressions=900, eligible_requests=1000, responses_served=900),
        "u3",
        custom_key,
        custom_value,
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
    assert not services.redis.exists(cache)
    assert maintain_price_rule_partitions.delay().get()["created"] >= 0


def test_parse_report_keeps_groone_try_rows() -> None:
    content = (
        "Dimension.DATE,Dimension.HOUR,Dimension.CUSTOM_CRITERIA,Dimension.AD_UNIT_ID,"
        "Dimension.COUNTRY_CODE\n"
        f"2026-11-01,7,content_hash={HASH},u3,BR\n"
        "2026-11-01,7,groone_try=3,u3,BR\n"
        "2026-11-01,7,utm_source=fb,u3,BR\n"
    )
    rows = list(parse_report(io.BytesIO(content.encode()), ReportKind.PRICE_RULE_HOURS))
    assert [(row.custom_key, row.custom_value) for row in rows] == [
        ("content_hash", HASH),
        ("groone_try", "3"),
    ]


def test_content_hash_and_groone_try_are_stored_in_the_same_call(services: Services) -> None:
    services._gam_writer = CurrencyWriter()  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    yesterday = days_ago(1)
    reports(services).rows[("123", ReportKind.PRICE_RULE_HOURS)] = [
        hour_row(yesterday, hour, key, value)
        for hour in range(4)
        for key, value in (("content_hash", HASH), ("groone_try", "3"))
    ]
    assert schedule_price_rule_hours.delay().get() == 1
    assert len(reports(services).calls) == 1
    assert count(services, "metrics.gam_key_value_hourly") == 8


def test_run_price_rules_forgets_cascade_cache_when_start_changed(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    site = enabled_site(services, client, network(services, client))
    fake_redis = FakeRedis()
    services.redis = fake_redis  # type: ignore[assignment]
    monkeypatch.setattr(price_rule_tasks, "run_site_cascades", lambda *_a, **_k: True)
    run_price_rules.delay().get()
    assert CASCADE_CACHE_KEY.format(site_id=site.id) in fake_redis.deleted


def test_run_price_rules_keeps_cascade_cache_when_start_did_not_change(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    enabled_site(services, client, network(services, client))
    fake_redis = FakeRedis()
    services.redis = fake_redis  # type: ignore[assignment]
    monkeypatch.setattr(price_rule_tasks, "run_site_cascades", lambda *_a, **_k: False)
    run_price_rules.delay().get()
    assert fake_redis.deleted == []


def test_run_price_rules_runs_cascades_after_the_site_rules(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    site = enabled_site(services, client, network(services, client))
    order: list[str] = []

    def record_cascades(*_args: Any, site_id: uuid.UUID, **_kwargs: Any) -> bool:
        """Anota a Cascata do site."""
        order.append(f"cascades:{site_id}")
        return False

    real_run = run_site_price_rules

    def record_rules(*args: Any, **kwargs: Any) -> list[str]:
        """Anota o motor das regras e delega ao real."""
        order.append("rules")
        return real_run(*args, **kwargs)

    monkeypatch.setattr(price_rule_tasks, "run_site_price_rules", record_rules)
    monkeypatch.setattr(price_rule_tasks, "run_site_cascades", record_cascades)
    run_price_rules.delay().get()
    assert order == ["rules", f"cascades:{site.id}"]


def test_run_price_rules_forgets_and_counts_hashes_when_a_cascade_fails(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    site = enabled_site(services, client, network(services, client))
    fake_redis = FakeRedis()
    services.redis = fake_redis  # type: ignore[assignment]

    def explode(*_args: Any, **_kwargs: Any) -> bool:
        """A Cascata falha."""
        raise RuntimeError("falhou")

    monkeypatch.setattr(price_rule_tasks, "run_site_price_rules", lambda *_a, **_k: [HASH])
    monkeypatch.setattr(price_rule_tasks, "run_site_cascades", explode)
    assert run_price_rules.delay().get() == 1
    assert fake_redis.deleted == [FLOOR_CACHE_KEY.format(site_id=site.id, content_hash=HASH)]


def test_create_price_rules_creates_cascades_too(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    site = enabled_site(services, client, network(services, client))
    created_for: list[uuid.UUID] = []

    def create_cascades(*_args: Any, site_id: uuid.UUID, **_kwargs: Any) -> int:
        """Anota o site e diz que criou duas Cascatas."""
        created_for.append(site_id)
        return 2

    monkeypatch.setattr(price_rule_tasks, "create_site_cascades", create_cascades)
    assert create_price_rules.delay().get() == 2
    assert created_for == [site.id]


def test_create_price_rules_keeps_the_count_when_a_cascade_fails(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = company(services)
    enabled_site(services, client, network(services, client))

    def explode(*_args: Any, **_kwargs: Any) -> int:
        """A criação das Cascatas falha."""
        raise RuntimeError("falhou")

    monkeypatch.setattr(price_rule_tasks, "create_site_price_rules", lambda *_a, **_k: 3)
    monkeypatch.setattr(price_rule_tasks, "create_site_cascades", explode)
    assert create_price_rules.delay().get() == 3


def network_time_zone(services: Services, network_id: uuid.UUID, company_id: uuid.UUID) -> Any:
    """O fuso gravado na network."""
    with services.uow(company_id) as uow:
        found = uow.networks.get(network_id)
        assert found is not None
        return found.time_zone


def test_sync_records_the_network_time_zone(services: Services) -> None:
    services._gam_writer = CurrencyWriter("America/Sao_Paulo")  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    assert schedule_price_rule_hours.delay().get() == 1
    assert network_time_zone(services, net.id, client.id) == "America/Sao_Paulo"


def test_sync_with_invalid_time_zone_logs_and_still_stores_hours(
    services: Services, caplog: pytest.LogCaptureFixture
) -> None:
    services._gam_writer = CurrencyWriter("Marte/Base")  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    reports(services).rows[("123", ReportKind.PRICE_RULE_HOURS)] = [
        hour_row(days_ago(1), hour) for hour in range(4)
    ]
    with caplog.at_level(logging.WARNING, logger="avant.worker.price_rules"):
        assert schedule_price_rule_hours.delay().get() == 1
    assert count(services, "metrics.gam_key_value_hourly") == 4
    assert network_time_zone(services, net.id, client.id) is None
    assert any("fuso" in record.getMessage() for record in caplog.records)


def test_sync_asks_gam_once_for_currency_and_time_zone(services: Services) -> None:
    writer = CurrencyWriter()
    services._gam_writer = writer  # type: ignore[assignment]
    services.redis = FakeRedis()  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    schedule_price_rule_hours.delay().get()
    schedule_price_rule_hours.delay().get()
    assert writer.calls == 1


def test_sync_survives_any_failure_recording_the_time_zone(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    services._gam_writer = CurrencyWriter()  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    reports(services).rows[("123", ReportKind.PRICE_RULE_HOURS)] = [
        hour_row(days_ago(1), hour) for hour in range(4)
    ]

    def not_found(*_args: Any, **_kwargs: Any) -> None:
        """A network some."""
        raise NotFound("network")

    monkeypatch.setattr(price_rule_tasks, "record_network_time_zone", not_found)
    assert schedule_price_rule_hours.delay().get() == 1
    assert count(services, "metrics.gam_key_value_hourly") == 4


def test_sync_does_not_ask_gam_again_when_the_time_zone_is_empty(services: Services) -> None:
    writer = CurrencyWriter("")
    services._gam_writer = writer  # type: ignore[assignment]
    fake_redis = FakeRedis()
    services.redis = fake_redis  # type: ignore[assignment]
    client = company(services)
    net = network(services, client)
    enabled_site(services, client, net)
    schedule_price_rule_hours.delay().get()
    schedule_price_rule_hours.delay().get()
    assert writer.calls == 1
    assert network_time_zone(services, net.id, client.id) is None


def test_target_network_reads_a_missing_time_zone_as_empty() -> None:
    from avant_worker.adapters.gam_writer import SoapGamWriter

    writer = SoapGamWriter("chave.json")
    writer._call = lambda *_a: {"currencyCode": "BRL", "effectiveRootAdUnitId": "9"}  # type: ignore[method-assign]
    target = writer.target_network("123")
    assert (target.currency_code, getattr(target, "time_zone", None)) == ("BRL", "")
