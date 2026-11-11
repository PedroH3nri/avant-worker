"""Key-values que a g-tag manda dos sites: os valores novos viram valores predefinidos no GAM.

O contrato com a avant-api, no Redis: ``kv:networks:connected`` (as networks que a rota aceita;
``refresh_key_value_networks`` mantém), ``kv:buffer:networks`` e ``kv:buffer:{network}`` (os pares
``key:value`` pendentes). ``kv:seen:{network}`` guarda por 24 horas o que já foi conferido, para
não ir ao banco a cada página. Os ids das keys vêm do GAM pelo nome, guardados por 1 hora.

Uma network sem acesso ao GAM (erro permanente) ganha ``kv:backoff:{network}`` por 30 minutos:
os pares ficam no buffer e ela não gasta cota a cada 30 s até a lista de conectadas tirá-la.
A trava ``key-values`` dura 10 minutos e é renovada a cada network; perdida, a execução para.
"""

import logging
import time
import uuid
from collections import defaultdict
from typing import cast

from avant_core.gam.client.errors import GamAccessDenied, GamNetworkNotFound
from avant_core.gam.key_values.services import (
    TRAFFIC_KEYS,
    connected_network_codes,
    register_traffic_key_values,
)
from celery.exceptions import SoftTimeLimitExceeded

from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.key_values")

CONNECTED = "kv:networks:connected"
PENDING_NETWORKS = "kv:buffer:networks"
BUFFER = "kv:buffer:{network}"
PROCESSING = "kv:processing:{network}:{run}"
SEEN = "kv:seen:{network}"
KEY_IDS = "kv:key-ids:{network}"
BACKOFF = "kv:backoff:{network}"
SEEN_FOR = 24 * 60 * 60
KEY_IDS_FOR = 60 * 60
BACKOFF_FOR = 30 * 60
LOCK_KEY = "key-values"
LOCK_FOR = 10 * 60
PERMANENT_ERRORS = (GamAccessDenied, GamNetworkNotFound)


@app.task(name="avant.gam.process_key_values")
def process_key_values() -> int:
    """A cada 30 s: esvazia o buffer de cada network e cria no GAM os valores novos; uma network
    que falha não para as outras, os pares dela voltam ao buffer e o erro permanente dá recuo."""
    services = get_services()
    if services.redis is None:
        return 0
    stored = 0
    with services.lock(LOCK_KEY, timeout=LOCK_FOR) as acquired:
        if not acquired:
            return 0
        for raw in cast(set[bytes], services.redis.smembers(PENDING_NETWORKS)):
            network = raw.decode() if isinstance(raw, bytes) else str(raw)
            if not services.renew_lock(LOCK_KEY, timeout=LOCK_FOR):
                log.warning("trava dos key-values perdida; o resto fica para a próxima execução")
                break
            if services.redis.exists(BACKOFF.format(network=network)):
                continue
            try:
                stored += _process_network(services, network)
            except SoftTimeLimitExceeded:
                raise
            except PERMANENT_ERRORS:
                services.redis.set(BACKOFF.format(network=network), 1, ex=BACKOFF_FOR)
                log.exception(
                    "network sem acesso ao GAM; recuo de 30 min", extra={"network": network}
                )
            except Exception:
                log.exception("key-values da network não foram criados", extra={"network": network})
    return stored


@app.task(name="avant.gam.refresh_key_value_networks")
def refresh_key_value_networks() -> int:
    """A cada 5 minutos: as networks conectadas (mais a da Groone) no Redis, para a rota."""
    services = get_services()
    groone = services.settings.gam_groone_network_code
    if services.redis is None or not groone:
        return 0
    codes = connected_network_codes(services.trusted_uow(), groone_network_code=groone)
    staging = f"{CONNECTED}:novo"
    pipe = services.redis.pipeline()
    pipe.delete(staging)
    pipe.sadd(staging, *codes)
    pipe.rename(staging, CONNECTED)
    pipe.execute()
    return len(codes)


def _process_network(services: Services, network: str) -> int:
    """Tira os pares do buffer (renomeando para uma chave só desta execução), descarta os vistos
    nas últimas 24 horas e manda o resto ao core; se o GAM falhar, devolve os pares ao buffer."""
    assert services.redis is not None
    client = services.redis
    buffer = BUFFER.format(network=network)
    processing = PROCESSING.format(network=network, run=uuid.uuid4().hex)
    client.srem(PENDING_NETWORKS, network)
    if not client.exists(buffer):
        return 0
    client.rename(buffer, processing)
    members = sorted(item.decode() for item in cast(set[bytes], client.smembers(processing)))
    client.delete(processing)
    seen, now = SEEN.format(network=network), time.time()
    client.zremrangebyscore(seen, 0, now - SEEN_FOR)
    scores = cast(list[float | None], client.zmscore(seen, members)) if members else []
    fresh = [member for member, score in zip(members, scores, strict=True) if score is None]
    if not fresh:
        return 0
    values: dict[str, set[str]] = defaultdict(set)
    for member in fresh:
        key, value = member.split(":", 1)
        values[key].add(value)
    try:
        key_ids = _key_ids(services, network)
        stored = register_traffic_key_values(
            services.trusted_uow(),
            writer=services.gam_writer,
            network_code=network,
            key_ids=key_ids,
            values=dict(values),
            clock=services.clock,
        )
    except Exception:
        client.sadd(buffer, *fresh)
        client.sadd(PENDING_NETWORKS, network)
        raise
    done = [member for member in fresh if member.split(":", 1)[0] in key_ids]
    if done:
        client.zadd(seen, {member: now for member in done})
    return stored


def _key_ids(services: Services, network: str) -> dict[str, str]:
    """Os ids das oito keys na network, lidos do GAM pelo nome e guardados por 1 hora."""
    assert services.redis is not None
    cached = cast(dict[bytes, bytes], services.redis.hgetall(KEY_IDS.format(network=network)))
    if cached:
        return {name.decode(): key_id.decode() for name, key_id in cached.items()}
    found = services.gam_writer.custom_keys(network, sorted(TRAFFIC_KEYS))
    if found:
        pipe = services.redis.pipeline()
        pipe.hset(KEY_IDS.format(network=network), mapping=found)
        pipe.expire(KEY_IDS.format(network=network), KEY_IDS_FOR)
        pipe.execute()
    return found
