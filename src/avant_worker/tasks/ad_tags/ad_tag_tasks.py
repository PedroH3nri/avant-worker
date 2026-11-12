"""Tarefas da ad tag (fila ``default``): as páginas vistas que o ``tag.js`` manda, as partições
da tabela crua e o cache da configuração pública.

O contrato com a avant-api, no Redis: a lista ``avant:page-views:buffer`` recebe um JSON por
página vista, com o resumo que o ``tag.js`` mandou (``key``, ``url``, ``page_view_id``,
``visitor_id``, ``session_id``, ``version``, ``device``, ``language``, ``referrer``,
``visible_ms``, ``scroll_percent``, ``clicked``, ``adblock``, ``id_post``, ``content_hash`` e
``blocks`` com ``type`` e ``state``), mais o ``ip`` de quem mandou e o ``received_at`` da API.
``flush_page_views`` renomeia a lista para ``avant:page-views:processing:{lote}``, acha o país
pelo IP (GeoLite2; o IP não é gravado), grava em pedaços com ``record_page_views`` e só então
apaga a chave. Cada página tem chave (dia, ``page_view_id``), então gravar o mesmo pedaço de
novo não soma duas vezes. A configuração de cada tag fica em ``avant:tag:{chave}``; a api apaga
ao publicar e pausar, e este worker depois de importar o inventário.

Todas usam ``trusted_uow``: o buffer e as partições são de todas as Empresas.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, cast

from avant_core.ad_tags.enums import AdTagBlockState, AdTagDevice
from avant_core.ad_tags.models import PageViewHit, PageViewHitBlock
from avant_core.ad_tags.services import network_ad_tag_keys, record_page_views
from avant_core.metrics.services import ensure_page_view_partitions

from avant_worker.app import app
from avant_worker.services import CountryLookup, Services, get_services

log = logging.getLogger("avant.worker.ad_tags")

BUFFER = "avant:page-views:buffer"
PROCESSING = "avant:page-views:processing:{batch}"
TAG_CACHE = "avant:tag:{key}"
CHUNK = 2_000
LOCK_SECONDS = 10 * 60
SOFT_LIMIT_SECONDS = 8 * 60
HARD_LIMIT_SECONDS = 9 * 60
TOTALS = ("stored", "duplicates", "skipped", "without_network")


@app.task(
    name="avant.default.flush_page_views",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def flush_page_views() -> dict[str, int]:
    """A cada minuto: grava as páginas vistas do buffer, primeiro os lotes que sobraram de uma
    execução anterior."""
    services = get_services()
    totals = dict.fromkeys(TOTALS, 0)
    with services.lock("page-views", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return totals
        client = services.redis
        pending = [key.decode() for key in client.scan_iter(PROCESSING.format(batch="*"))]
        if client.exists(BUFFER):
            fresh = PROCESSING.format(batch=uuid.uuid4().hex)
            client.rename(BUFFER, fresh)
            pending.append(fresh)
        for key in pending:
            for name, count in _flush(services, key).items():
                totals[name] += count
    if any(totals.values()):
        log.info("visitas da tag gravadas", extra=totals)
    return totals


@app.task(
    name="avant.default.ensure_page_view_partitions",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def ensure_page_view_partitions_task() -> int:
    """Uma vez por dia: cria as partições diárias de hoje e dos 7 dias seguintes que faltam."""
    services = get_services()
    created = ensure_page_view_partitions(services.trusted_uow(), clock=services.clock)
    if created:
        log.info("partições das visitas criadas", extra={"created": created})
    return created


def forget_network_ad_tags(services: Services, network_id: uuid.UUID) -> int:
    """Depois de importar o inventário da network: apaga o cache das tags dos sites dela. Falhar
    aqui não falha a importação (o cache expira em 1 hora)."""
    try:
        tag_keys = network_ad_tag_keys(services.trusted_uow(), network_id=network_id)
        cache_keys = [TAG_CACHE.format(key=key) for key in tag_keys]
        return cast(int, services.redis.delete(*cache_keys)) if cache_keys else 0
    except Exception:
        log.exception("cache das ad tags não foi apagado", extra={"network_id": str(network_id)})
        return 0


def _flush(services: Services, key: str) -> dict[str, int]:
    """Grava a lista da chave em pedaços e apaga a chave no fim."""
    totals = dict.fromkeys(TOTALS, 0)
    raw = cast(list[bytes], services.redis.lrange(key, 0, -1))
    countries = services.countries
    for start in range(0, len(raw), CHUNK):
        hits, broken = _hits(raw[start : start + CHUNK], countries)
        result = record_page_views(services.trusted_uow(), hits=hits, clock=services.clock)
        totals["stored"] += result.stored
        totals["duplicates"] += result.duplicates
        totals["skipped"] += result.skipped + broken
        totals["without_network"] += result.without_network
    services.redis.delete(key)
    return totals


def _hits(raw: list[bytes], countries: CountryLookup | None) -> tuple[list[PageViewHit], int]:
    """As páginas que estão no formato e quantas não estavam."""
    hits: list[PageViewHit] = []
    broken = 0
    for item in raw:
        try:
            hits.append(_hit(json.loads(item), countries))
        except (ValueError, KeyError, TypeError, AttributeError):
            broken += 1
    return hits, broken


def _hit(data: dict[str, Any], countries: CountryLookup | None) -> PageViewHit:
    """A página vista do JSON que a api guardou, com o país no lugar do IP."""
    country = countries.country(data.get("ip")) if countries is not None else None
    version = data.get("version")
    return PageViewHit(
        key=str(data["key"]),
        url=str(data["url"]),
        page_view_id=uuid.UUID(data["page_view_id"]),
        visitor_id=uuid.UUID(data["visitor_id"]),
        session_id=uuid.UUID(data["session_id"]),
        received_at=_received_at(data["received_at"]),
        device=AdTagDevice(data["device"]),
        country=country or "",
        version=int(version) if version is not None else None,
        referrer=_optional_text(data.get("referrer")),
        language=_optional_text(data.get("language")),
        visible_ms=int(data.get("visible_ms") or 0),
        scroll_percent=int(data.get("scroll_percent") or 0),
        clicked=bool(data.get("clicked")),
        adblock=bool(data.get("adblock")),
        id_post=_optional_text(data.get("id_post")),
        content_hash=_optional_text(data.get("content_hash")),
        blocks=tuple(
            PageViewHitBlock(str(block["type"]), AdTagBlockState(block["state"]))
            for block in data.get("blocks") or []
        ),
    )


def _received_at(value: str) -> datetime:
    """A hora em que a API recebeu, sempre com fuso."""
    received = datetime.fromisoformat(value)
    if received.tzinfo is None:
        raise ValueError("received_at sem fuso")
    return received


def _optional_text(value: object) -> str | None:
    """O texto como veio, ou vazio."""
    return str(value) if value is not None else None
