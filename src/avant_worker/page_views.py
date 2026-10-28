"""Leitura das visitas no Mongo do iGroone/data (contador do PageViewsV2). Só leitura.

O data soma cada visita no Redis e grava de tempos em tempos em ``page_views_v2_domains``:
um documento por domínio, network, data e hora de São Paulo e país (nome do GeoLite), com
``count`` acumulado. A hora chega como texto (``"09"``).
"""

from collections.abc import Iterable
from datetime import date
from typing import Any

from avant_core.metrics.models import PageViewCount
from pymongo import MongoClient

DOMAINS_COLLECTION = "page_views_v2_domains"
TIMEOUT_MS = 10_000


class MongoPageViews:
    """Contagens de visitas por network e período, direto da coleção do data."""

    def __init__(self, url: str, database: str) -> None:
        self._client: MongoClient[dict[str, Any]] = MongoClient(
            url, serverSelectionTimeoutMS=TIMEOUT_MS, socketTimeoutMS=TIMEOUT_MS * 3
        )
        self._collection = self._client[database][DOMAINS_COLLECTION]

    def counts(self, network_code: str, start: date, end: date) -> list[PageViewCount]:
        """Visitas por domínio, hora e país da network entre ``start`` e ``end`` (inclusive)."""
        documents = self._collection.find(
            {"network": network_code, "date": {"$gte": start.isoformat(), "$lte": end.isoformat()}},
            projection={
                "_id": False,
                "domain": True,
                "date": True,
                "hour": True,
                "country": True,
                "count": True,
            },
        )
        return parse_documents(documents)


def parse_documents(documents: Iterable[dict[str, Any]]) -> list[PageViewCount]:
    """Converte os documentos do Mongo; os que não têm data ou hora válida ficam de fora."""
    counts: list[PageViewCount] = []
    for document in documents:
        try:
            day = date.fromisoformat(str(document["date"]))
            hour = int(str(document["hour"]))
            page_views = int(document.get("count") or 0)
        except (KeyError, ValueError):
            continue
        counts.append(
            PageViewCount(
                domain=str(document.get("domain") or ""),
                date=day,
                hour=hour,
                country=str(document.get("country") or ""),
                page_views=page_views,
            )
        )
    return counts
