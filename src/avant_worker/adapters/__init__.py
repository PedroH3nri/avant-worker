"""Adaptadores do worker: GAM (REST e relatórios SOAP), visitas do data, cotações e eventos."""

from avant_worker.adapters.events import channel, publish
from avant_worker.adapters.exchange_rates import ExchangeRatesUnavailable, OpenExchangeRates
from avant_worker.adapters.gam_client import RestGamClient
from avant_worker.adapters.gam_reports import (
    ReportKind,
    SoapReportClient,
    parse_report,
    report_query,
)
from avant_worker.adapters.page_views import MongoPageViews, parse_documents

__all__ = [
    "ExchangeRatesUnavailable",
    "MongoPageViews",
    "OpenExchangeRates",
    "ReportKind",
    "RestGamClient",
    "SoapReportClient",
    "channel",
    "parse_documents",
    "parse_report",
    "publish",
    "report_query",
]
