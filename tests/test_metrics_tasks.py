from datetime import date, timedelta
from typing import Any

from avant_core.gam.client.errors import GamAccessDenied, GamUnavailable
from avant_core.gam.networks.enums import ConnectionType, Delegation
from avant_core.gam.networks.models import Network
from avant_core.metrics.models import GamCounts, GamReportRow
from sqlalchemy import text

from avant_worker.adapters import ReportKind, parse_report, report_query
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.gam import sync_network
from avant_worker.tasks.metrics import (
    backfill_metrics,
    schedule_metrics,
    schedule_reprocess,
    sync_metrics,
)
from tests.fake_gam import FakeReports
from tests.test_gam_tasks import company, count, fake, inventory, network

DAY = date(2026, 11, 1)

AD_UNIT_CSV = (
    "Dimension.DATE,Dimension.DEVICE_CATEGORY_NAME,Dimension.AD_UNIT_ID,Ad unit 1,Ad unit 2,"
    "Dimension.COUNTRY_CODE,Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE,"
    "Column.AD_EXCHANGE_LINE_ITEM_LEVEL_IMPRESSIONS,"
    "Column.TOTAL_INVENTORY_LEVEL_UNFILLED_IMPRESSIONS,"
    "Column.PROGRAMMATIC_RESPONSES_SERVED,Column.TOTAL_PROGRAMMATIC_ELIGIBLE_AD_REQUESTS,"
    "Column.AD_EXCHANGE_LINE_ITEM_LEVEL_CLICKS,"
    "Column.AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS,"
    "Column.AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS\n"
    "2026-11-01,Desktop,u2,acai.com.br,topo,BR,1500000,100,5,90,120,3,70,95\n"
    "2026-11-01,Smartphone,u1,acai.com.br,,US,-,1,0,1,1,0,0,0\n"
)


def reports(services: Services) -> FakeReports:
    source = services.reports
    assert isinstance(source, FakeReports)
    return source


def row(gam_id: str, revenue: int, **custom: str) -> GamReportRow:
    return GamReportRow(
        DAY,
        "acai.com.br/topo",
        "BR",
        "Desktop",
        revenue,
        GamCounts(impressions=10),
        gam_id,
        custom.get("key"),
        custom.get("value"),
    )


def test_parse_ad_unit_report() -> None:
    first, second = parse_report(AD_UNIT_CSV.encode(), ReportKind.AD_UNIT)
    assert first.ad_unit_path == "acai.com.br/topo" and first.gam_ad_unit_id == "u2"
    assert first.revenue_micros == 1_500_000 and first.country_code == "BR"
    assert first.counts == GamCounts(100, 5, 70, 95, 3, 120, 90)
    assert second.ad_unit_path == "acai.com.br" and second.revenue_micros == 0


def test_parse_key_value_report_skips_rows_without_criteria() -> None:
    content = (
        "Dimension.DATE,Dimension.DEVICE_CATEGORY_NAME,Dimension.CUSTOM_CRITERIA,"
        "Dimension.AD_UNIT_ID,Dimension.AD_UNIT_NAME,Dimension.COUNTRY_CODE\n"
        "2026-11-01,Tablet,utm_source=fb=x,u1,acai.com.br,BR\n"
        "2026-11-01,Tablet,,u1,acai.com.br,BR\n"
    )
    (only,) = parse_report(("﻿" + content).encode(), ReportKind.KEY_VALUE)
    assert (only.custom_key, only.custom_value) == ("utm_source", "fb=x")
    assert only.ad_unit_path == "acai.com.br" and only.revenue_micros == 0


def test_report_query_matches_unified_sync() -> None:
    query = report_query(ReportKind.KEY_VALUE, DAY, DAY + timedelta(days=1))
    assert query["dimensions"][2] == "CUSTOM_CRITERIA"
    assert query["adUnitView"] == "HIERARCHICAL" and query["reportCurrency"] == "USD"
    assert query["endDate"] == {"year": 2026, "month": 11, "day": 2}
    assert len(query["columns"]) == 8
    assert "CUSTOM_CRITERIA" not in report_query(ReportKind.AD_UNIT, DAY, DAY)["dimensions"]


def test_metrics_tasks_are_registered_on_the_gam_queue() -> None:
    app.loader.import_default_modules()
    for name in (
        "avant.gam.sync_metrics",
        "avant.gam.backfill_metrics",
        "avant.gam.schedule_metrics",
        "avant.gam.schedule_reprocess",
    ):
        assert name in app.tasks and _route(name) == {"queue": "gam"}
    task: Any = sync_metrics
    assert task.autoretry_for == (GamUnavailable,) and task.max_retries == 4


def test_sync_metrics_stores_both_reports_idempotently(services: Services) -> None:
    owner = company(services)
    connected = network(services, owner)
    inventory(fake(services))
    sync_network.delay(str(owner.id), str(connected.id)).get()
    source = reports(services)
    source.rows[("123", ReportKind.AD_UNIT)] = [row("u2", 1_000_000), row("u2", 500_000)]
    source.rows[("123", ReportKind.KEY_VALUE)] = [row("u2", 10, key="utm_source", value="fb")]

    result = sync_metrics.delay(str(owner.id), str(connected.id), "2026-11-01", "2026-11-02").get()
    assert (result["daily_rows"], result["key_value_rows"]) == (1, 1)
    assert result["rows_without_site"] == 0
    assert [call[1] for call in source.calls] == [ReportKind.AD_UNIT, ReportKind.KEY_VALUE]
    sync_metrics.delay(str(owner.id), str(connected.id), "2026-11-01", "2026-11-02").get()
    assert count(services, "metrics.gam_daily") == 1
    assert count(services, "metrics.gam_key_value_daily") == 1
    with services.uow(owner.id) as uow:
        gross_revenue = uow.session.execute(
            text("SELECT revenue_micros, site_id IS NOT NULL FROM metrics.gam_daily")
        ).one()
    assert tuple(gross_revenue) == (1_500_000, True)


def test_sync_metrics_skips_manage_inventory_and_records_permanent_errors(
    services: Services,
) -> None:
    owner = company(services)
    managed = Network(
        company_id=owner.id,
        network_code="456",
        connection_type=ConnectionType.MCM,
        delegation=Delegation.MANAGE_INVENTORY,
        created_at=services.clock.now(),
    )
    with services.uow(owner.id) as uow:
        uow.networks.add(managed)
        uow.commit()
    skipped = sync_metrics.delay(str(owner.id), str(managed.id), "2026-11-01", "2026-11-01")
    assert skipped.get() == {"skipped": "manage_inventory"}

    connected = network(services, owner)
    reports(services).fail_next.append(GamAccessDenied("sem acesso"))
    failed = sync_metrics.delay(str(owner.id), str(connected.id), "2026-11-01", "2026-11-01")
    assert failed.get() == {"error": "gam_access_denied"}


def test_backfill_splits_the_period_in_weekly_chunks(services: Services) -> None:
    owner = company(services)
    connected = network(services, owner)
    assert backfill_metrics.delay(str(owner.id), str(connected.id), days=15).get() == 3
    periods = [(call[2], call[3]) for call in reports(services).calls[::2]]
    today = services.clock.now().date()
    assert periods[0] == (today - timedelta(days=7), today - timedelta(days=1))
    assert periods[-1] == (today - timedelta(days=15), today - timedelta(days=15))


def test_schedules_cover_today_and_the_reprocess_window(services: Services) -> None:
    owner = company(services)
    network(services, owner)
    assert schedule_metrics.delay().get() == 1
    assert schedule_reprocess.delay().get() == 1
    today = services.clock.now().date()
    periods = {(call[2], call[3]) for call in reports(services).calls}
    assert (today - timedelta(days=1), today) in periods
    assert (today - timedelta(days=4), today - timedelta(days=2)) in periods
