from datetime import UTC, date, datetime

import httpx
from avant_core.gam.networks.enums import Delegation
from avant_core.metrics.models import GamMcmEarning
from google.auth.credentials import AnonymousCredentials

from avant_worker.app import _route, app
from avant_worker.gam_client import BASE_URL, RestGamClient
from avant_worker.services import Services
from avant_worker.tasks.earnings import BACKFILL_MONTHS, months_to_fetch, sync_mcm_earnings
from tests.conftest import GROONE_NETWORK
from tests.fake_gam import FakeEarnings
from tests.test_gam_tasks import company, count, network

TODAY = date(2026, 10, 15)
SEPTEMBER = date(2026, 9, 1)


def test_months_backfill_then_previous_month_again() -> None:
    first_run = months_to_fetch(None, TODAY)
    assert len(first_run) == BACKFILL_MONTHS + 1
    assert (first_run[0], first_run[-1]) == (date(2025, 9, 1), SEPTEMBER)
    assert months_to_fetch(SEPTEMBER, TODAY) == [SEPTEMBER]
    assert months_to_fetch(date(2026, 7, 1), TODAY) == [
        date(2026, 7, 1),
        date(2026, 8, 1),
        SEPTEMBER,
    ]
    assert months_to_fetch(date(2026, 1, 1), date(2026, 1, 20)) == [date(2025, 12, 1)]


def test_client_reads_mcm_earnings_money_in_micros() -> None:
    def reply(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/networks/9999/mcmEarnings:fetch"
        assert request.url.params["month.year"] == "2026"
        assert request.url.params["month.month"] == "9"
        body = {
            "mcmEarnings": [
                {
                    "child": "networks/123",
                    "month": {"year": 2026, "month": 9, "day": 1},
                    "delegationType": "MANAGE_INVENTORY",
                    "totalEarnings": {"currencyCode": "USD", "units": "10", "nanos": 500000000},
                    "deductions": {"currencyCode": "USD", "nanos": 400000000},
                    "childPayment": {"currencyCode": "USD", "units": "7"},
                    "parentPayment": {"currencyCode": "USD", "units": "3", "nanos": 100000000},
                }
            ]
        }
        return httpx.Response(200, json=body)

    http = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(reply))
    client = RestGamClient(AnonymousCredentials(), service_account_email="sa@x", http=http)  # type: ignore[no-untyped-call]
    assert list(client.list_mcm_earnings("9999", SEPTEMBER)) == [
        GamMcmEarning(
            month=SEPTEMBER,
            child_network_code="123",
            delegation=Delegation.MANAGE_INVENTORY,
            currency="USD",
            total_earnings_micros=10_500_000,
            deductions_micros=400_000,
            child_payment_micros=7_000_000,
            parent_payment_micros=3_100_000,
        )
    ]


def test_earnings_task_is_on_the_gam_queue() -> None:
    app.loader.import_default_modules()
    assert _route("avant.gam.sync_mcm_earnings") == {"queue": "gam"}
    schedule = app.conf.beat_schedule["gam-sync-mcm-earnings"]
    assert schedule["task"] == "avant.gam.sync_mcm_earnings"


def test_sync_stores_the_month_for_networks_in_avant(services: Services) -> None:
    source = services.earnings
    assert isinstance(source, FakeEarnings)
    assert sync_mcm_earnings.delay().get() == {"skipped": "not_configured"}
    services.settings = services.settings.model_copy(
        update={"gam_groone_network_code": GROONE_NETWORK}
    )
    client = company(services)
    network(services, client, "123")
    source.by_month[SEPTEMBER] = [
        GamMcmEarning(SEPTEMBER, "123", Delegation.MANAGE_ACCOUNT, "USD", 1_000, 40, 700, 260),
        GamMcmEarning(SEPTEMBER, "555", None, "USD", 1_000, 0, 800, 200),
    ]
    result = sync_mcm_earnings.delay("2026-09").get()
    assert result == {"months": 1, "rows": 1, "unknown_networks": 1}
    assert source.calls == [(GROONE_NETWORK, SEPTEMBER)]
    assert count(services, "metrics.mcm_earnings") == 1
    services.clock = _FixedClock(datetime(2026, 10, 15, 3, 10, tzinfo=UTC))
    assert sync_mcm_earnings.delay().get()["months"] == 1
    assert source.calls[-1] == (GROONE_NETWORK, SEPTEMBER)


class _FixedClock:
    """Relógio parado num instante."""

    def __init__(self, instant: datetime) -> None:
        self._instant = instant

    def now(self) -> datetime:
        """O instante fixo."""
        return self._instant
