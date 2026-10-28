"""Cotações de cada dia no Open Exchange Rates (base USD), como o CurrenciesSync do Genius.

A chave (``OPENEXCHANGERATES_APP_ID``) fica só nas VMs. ``latest`` é a cotação de agora e
``historical`` a do fim de um dia já fechado.
"""

import json
from datetime import date
from decimal import Decimal

import httpx
from avant_core.money.catalog import CURRENCIES

BASE_URL = "https://openexchangerates.org/api/"

SYMBOLS = ",".join(currency.code for currency in CURRENCIES)


class ExchangeRatesUnavailable(RuntimeError):
    """O Open Exchange Rates não respondeu ou respondeu sem cotações."""


class OpenExchangeRates:
    """Cliente HTTP do Open Exchange Rates, só com as moedas do painel."""

    def __init__(self, app_id: str, http: httpx.Client | None = None) -> None:
        self._app_id = app_id
        self._http = http or httpx.Client(base_url=BASE_URL, timeout=30.0)

    def latest(self) -> dict[str, Decimal]:
        """Cotações de agora (1 USD na moeda)."""
        return self._rates("latest.json")

    def historical(self, day: date) -> dict[str, Decimal]:
        """Cotações do fim do dia (1 USD na moeda)."""
        return self._rates(f"historical/{day.isoformat()}.json")

    def _rates(self, path: str) -> dict[str, Decimal]:
        """Pede as cotações e lê os números como Decimal, sem passar por float."""
        try:
            response = self._http.get(path, params={"app_id": self._app_id, "symbols": SYMBOLS})
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExchangeRatesUnavailable(f"Open Exchange Rates falhou: {path}") from exc
        body = json.loads(response.text, parse_float=Decimal, parse_int=Decimal)
        rates = body.get("rates") if isinstance(body, dict) else None
        if not isinstance(rates, dict) or not rates:
            raise ExchangeRatesUnavailable(f"Open Exchange Rates sem cotações: {path}")
        return {str(code): Decimal(value) for code, value in rates.items()}
