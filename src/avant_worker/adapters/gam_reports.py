"""Relatórios de métricas do Google Ad Manager pela API SOAP (ReportService).

A API REST v1 cria um objeto ``Report`` na network do cliente para cada relatório, ou
seja, escreve no GAM. O SOAP só roda o relatório e baixa o resultado, como o unified-sync
faz hoje com a mesma biblioteca (``googleads``). Este módulo só chama ``runReportJob``,
``getReportJobStatus`` e ``getReportDownloadUrlWithOptions``.

Os relatórios são os dois do unified-sync: por ad unit e por key-value, com as mesmas
oito colunas, em USD e com os ad units hierárquicos (``Ad unit 1``, ``Ad unit 2``...).
"""

import csv
import gzip
import io
import logging
import time
from collections.abc import Iterator
from datetime import date
from enum import StrEnum
from typing import Any

from avant_core.gam.client.errors import (
    GamAccessDenied,
    GamError,
    GamNetworkNotFound,
    GamUnavailable,
)
from avant_core.metrics.models import GamCounts, GamReportRow
from avant_core.metrics.models.gam_daily_metric import REPORT_CURRENCY
from google.auth import exceptions as auth_exceptions
from googleads import ad_manager, errors, oauth2

APPLICATION_NAME = "Groone Avant"

POLL_SECONDS = 5

MAX_HIERARCHY_LEVELS = 10

COLUMN_PREFIX = "Column."

DIMENSION_PREFIX = "Dimension."

COUNT_COLUMNS = {
    "impressions": "AD_EXCHANGE_LINE_ITEM_LEVEL_IMPRESSIONS",
    "unfilled_impressions": "TOTAL_INVENTORY_LEVEL_UNFILLED_IMPRESSIONS",
    "viewable_impressions": "AD_EXCHANGE_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS",
    "measurable_impressions": "AD_EXCHANGE_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS",
    "clicks": "AD_EXCHANGE_LINE_ITEM_LEVEL_CLICKS",
    "eligible_requests": "TOTAL_PROGRAMMATIC_ELIGIBLE_AD_REQUESTS",
    "responses_served": "PROGRAMMATIC_RESPONSES_SERVED",
}

REVENUE_COLUMN = "AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE"

ACCESS_DENIED_MARKERS = ("AuthenticationError", "PermissionError", "PERMISSION_DENIED")

NOT_FOUND_MARKERS = ("NETWORK_NOT_FOUND", "NO_NETWORKS_TO_ACCESS", "NETWORK_CODE_NOT_FOUND")

TEMPORARY_MARKERS = ("QuotaError", "ServerError", "InternalApiError", "EXCEEDED_QUOTA")

log = logging.getLogger("avant.worker.gam")


class ReportKind(StrEnum):
    """Os dois relatórios do unified-sync."""

    AD_UNIT = "ad_unit"
    KEY_VALUE = "key_value"


class SoapReportClient:
    """Roda e baixa relatórios; um cliente do googleads por network, como no unified-sync."""

    def __init__(self, key_file: str, *, version: str | None = None) -> None:
        self._key_file = key_file
        self._version = version or sorted(ad_manager._SERVICE_MAP)[-1]
        self._oauth: oauth2.GoogleServiceAccountClient | None = None

    def report(
        self, network_code: str, kind: ReportKind, start: date, end: date
    ) -> Iterator[GamReportRow]:
        """Linhas do relatório do período, já no formato do avant-core."""
        content = self._download(network_code, report_query(kind, start, end))
        yield from parse_report(content, kind)

    def _download(self, network_code: str, query: dict[str, Any]) -> bytes:
        """Roda o relatório na network, espera terminar e devolve o CSV descomprimido."""
        started = time.monotonic()
        try:
            downloader = self._client(network_code).GetDataDownloader(version=self._version)
            job_id = downloader.WaitForReport({"reportQuery": query}, POLL_SECONDS)
            buffer = io.BytesIO()
            downloader.DownloadReportToFile(job_id, "CSV_DUMP", buffer)
        except errors.AdManagerReportError as error:
            raise GamUnavailable(f"o relatório falhou no GAM: {error}") from error
        except errors.GoogleAdsServerFault as error:
            raise _classify(network_code, error) from error
        except auth_exceptions.RefreshError as error:
            raise GamAccessDenied(f"a conta de serviço não autenticou: {error}") from error
        except (auth_exceptions.TransportError, OSError) as error:
            raise GamUnavailable(f"falha de rede no relatório: {error}") from error
        log.info(
            "relatório do GAM baixado",
            extra={
                "network_code": network_code,
                "ms": round((time.monotonic() - started) * 1000),
                "bytes": buffer.tell(),
            },
        )
        return gzip.decompress(buffer.getvalue())

    def _client(self, network_code: str) -> ad_manager.AdManagerClient:
        """Cliente do googleads da network, reaproveitando o token da conta de serviço."""
        if self._oauth is None:
            self._oauth = oauth2.GoogleServiceAccountClient(
                self._key_file, oauth2.GetAPIScope("ad_manager")
            )
        return ad_manager.AdManagerClient(self._oauth, APPLICATION_NAME, network_code=network_code)


def report_query(kind: ReportKind, start: date, end: date) -> dict[str, Any]:
    """O mesmo ``reportQuery`` do unified-sync, com o id do ad unit e o código do país."""
    dimensions = ["DATE", "DEVICE_CATEGORY_NAME", "AD_UNIT_ID", "AD_UNIT_NAME", "COUNTRY_CODE"]
    if kind is ReportKind.KEY_VALUE:
        dimensions.insert(2, "CUSTOM_CRITERIA")
    return {
        "dimensions": dimensions,
        "columns": [REVENUE_COLUMN, *COUNT_COLUMNS.values()],
        "adUnitView": "HIERARCHICAL",
        "dateRangeType": "CUSTOM_DATE",
        "startDate": _soap_date(start),
        "endDate": _soap_date(end),
        "reportCurrency": REPORT_CURRENCY,
    }


def parse_report(content: bytes, kind: ReportKind) -> Iterator[GamReportRow]:
    """Lê o CSV_DUMP; no relatório por key-value, linha sem ``chave=valor`` fica de fora."""
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    for record in reader:
        custom_key: str | None = None
        custom_value: str | None = None
        if kind is ReportKind.KEY_VALUE:
            criteria = record.get(f"{DIMENSION_PREFIX}CUSTOM_CRITERIA") or ""
            if "=" not in criteria:
                continue
            custom_key, custom_value = criteria.split("=", 1)
        yield GamReportRow(
            date=date.fromisoformat(record[f"{DIMENSION_PREFIX}DATE"]),
            ad_unit_path=_ad_unit_path(record),
            country_code=record.get(f"{DIMENSION_PREFIX}COUNTRY_CODE") or "",
            device=record.get(f"{DIMENSION_PREFIX}DEVICE_CATEGORY_NAME") or "",
            revenue_micros=_integer(record.get(f"{COLUMN_PREFIX}{REVENUE_COLUMN}")),
            counts=GamCounts(
                **{
                    field: _integer(record.get(f"{COLUMN_PREFIX}{column}"))
                    for field, column in COUNT_COLUMNS.items()
                }
            ),
            gam_ad_unit_id=record.get(f"{DIMENSION_PREFIX}AD_UNIT_ID") or None,
            custom_key=custom_key,
            custom_value=custom_value,
        )


def _ad_unit_path(record: dict[str, str]) -> str:
    """``acai.com.br/topo`` a partir das colunas ``Ad unit 1``, ``Ad unit 2``..."""
    levels = [
        record[f"Ad unit {level}"]
        for level in range(1, MAX_HIERARCHY_LEVELS + 1)
        if record.get(f"Ad unit {level}")
    ]
    return "/".join(levels) or record.get(f"{DIMENSION_PREFIX}AD_UNIT_NAME") or ""


def _integer(value: str | None) -> int:
    """Número do CSV; vazio ou ``-`` vira zero."""
    try:
        return int(float(value or 0))
    except ValueError:
        return 0


def _soap_date(day: date) -> dict[str, int]:
    """Data no formato do SOAP do GAM."""
    return {"year": day.year, "month": day.month, "day": day.day}


def _classify(network_code: str, error: errors.GoogleAdsServerFault) -> GamError:
    """Converte a falha do SOAP em erro do avant-core, temporário ou não."""
    text = f"{network_code}: {error}"
    if any(marker in text for marker in NOT_FOUND_MARKERS):
        return GamNetworkNotFound(text)
    if any(marker in text for marker in ACCESS_DENIED_MARKERS):
        return GamAccessDenied(text)
    if any(marker in text for marker in TEMPORARY_MARKERS):
        return GamUnavailable(text)
    return GamError(text)
