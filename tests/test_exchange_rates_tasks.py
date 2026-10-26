from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import httpx
import pytest
from sqlalchemy import text

from avant_worker.app import _route, app
from avant_worker.exchange_rates import ExchangeRatesUnavailable, OpenExchangeRates
from avant_worker.services import Services
from avant_worker.tasks.exchange_rates import (
    BACKFILL_DAYS,
    closed_days_to_fetch,
    sync_exchange_rates,
)
from tests.fake_gam import FakeExchangeRates

TODAY = date(2026, 11, 2)


def test_closed_days_backfill_then_only_what_is_missing() -> None:
    first_run = closed_days_to_fetch(None, TODAY)
    assert len(first_run) == BACKFILL_DAYS
    assert first_run[-1] == TODAY - timedelta(days=1)
    assert closed_days_to_fetch(TODAY - timedelta(days=1), TODAY) == [TODAY - timedelta(days=1)]
    assert closed_days_to_fetch(TODAY, TODAY) == []
    assert len(closed_days_to_fetch(date(2025, 1, 1), TODAY)) == BACKFILL_DAYS


def test_client_reads_rates_as_decimals_and_fails_clearly() -> None:
    def reply(request: httpx.Request) -> httpx.Response:
        assert request.url.params["app_id"] == "chave"
        assert "BRL" in request.url.params["symbols"]
        if request.url.path.endswith("2026-11-01.json"):
            return httpx.Response(200, text='{"base": "USD", "rates": {"BRL": 5.3123, "USD": 1}}')
        return httpx.Response(401, text='{"error": true}')

    http = httpx.Client(
        base_url="https://openexchangerates.org/api/", transport=httpx.MockTransport(reply)
    )
    client = OpenExchangeRates("chave", http)
    assert client.historical(date(2026, 11, 1)) == {"BRL": Decimal("5.3123"), "USD": Decimal(1)}
    with pytest.raises(ExchangeRatesUnavailable):
        client.latest()


def test_exchange_rates_task_is_on_the_default_queue() -> None:
    app.loader.import_default_modules()
    assert _route("avant.default.sync_exchange_rates") == {"queue": "default"}
    schedule = app.conf.beat_schedule["exchange-rates-sync"]
    assert schedule["task"] == "avant.default.sync_exchange_rates"


def test_sync_stores_closed_days_and_today(services: Services) -> None:
    source = services.exchange_rates
    assert isinstance(source, FakeExchangeRates)
    assert sync_exchange_rates.delay().get() == {"closed_days": BACKFILL_DAYS}
    today = datetime.now(UTC).date()
    with services.engine.connect() as conn:
        rows = conn.execute(
            text("SELECT date, code, rate FROM metrics.exchange_rates WHERE date >= :start"),
            {"start": today - timedelta(days=1)},
        ).all()
    assert {(row.date, row.code, row.rate) for row in rows} == {
        (today - timedelta(days=1), "BRL", Decimal("4.5")),
        (today - timedelta(days=1), "EUR", Decimal("0.9")),
        (today - timedelta(days=1), "USD", Decimal(1)),
        (today, "BRL", Decimal("5")),
        (today, "USD", Decimal(1)),
    }
    source.days.clear()
    assert sync_exchange_rates.delay().get() == {"closed_days": 0}
    assert source.days == []


def test_sync_without_key_does_nothing(services: Services) -> None:
    services._exchange_rates = None
    assert sync_exchange_rates.delay().get() == {"skipped": "not_configured"}
