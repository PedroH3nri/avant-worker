"""Adaptadores do worker: GAM (REST, relatórios SOAP e as escritas SOAP das ferramentas),
visitas do data, cotações, eventos e as páginas dos sites (checklist)."""

from avant_worker.adapters.events import channel, publish
from avant_worker.adapters.exchange_rates import ExchangeRatesUnavailable, OpenExchangeRates
from avant_worker.adapters.gam_client import RestGamClient
from avant_worker.adapters.gam_reports import (
    METRIC_REPORTS,
    ReportKind,
    SoapReportClient,
    parse_report,
    report_query,
)
from avant_worker.adapters.gam_writer import SoapGamWriter
from avant_worker.adapters.page_fetcher import HttpPageFetcher
from avant_worker.adapters.page_views import MongoPageViews, parse_documents

__all__ = [
    "METRIC_REPORTS",
    "ExchangeRatesUnavailable",
    "HttpPageFetcher",
    "MongoPageViews",
    "OpenExchangeRates",
    "ReportKind",
    "RestGamClient",
    "SoapGamWriter",
    "SoapReportClient",
    "channel",
    "parse_documents",
    "parse_report",
    "publish",
    "report_query",
]
