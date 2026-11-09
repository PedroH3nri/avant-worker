"""Eventos e contatos que o script do reward manda, e o cache das páginas de reward.

O contrato com a avant-api, no Redis: a lista ``avant:reward:buffer`` recebe um JSON por item
(``{"type": "event", ...}`` ou ``{"type": "lead", ...}``). Esta tarefa renomeia a lista para
``avant:reward:processing:{lote}``, grava no banco em pedaços (cada um com o seu identificador,
o que torna a gravação idempotente) e só então apaga a chave; uma chave de processamento que
sobrou de uma execução que caiu é gravada de novo na próxima. A configuração de cada página fica
em ``avant:reward:{domínio}/{caminho}``; a api apaga ao salvar e este worker depois de importar o
inventário.
"""

import json
import logging
import uuid
from datetime import date, datetime, timedelta
from typing import Any, cast

from avant_core.rewards.enums import RewardEventKind
from avant_core.rewards.models import RewardBatch, RewardEvent, RewardLeadSubmission
from avant_core.rewards.services import (
    latest_reward_pages,
    purge_reward_batches,
    record_reward_batch,
)

from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.rewards")

BUFFER = "avant:reward:buffer"
PROCESSING = "avant:reward:processing:{batch}"
PAGE = "avant:reward:{domain}/{path}"
CHUNK = 5_000
LOCK_FOR = 10 * 60
KEEP_BATCHES = timedelta(days=7)


@app.task(name="avant.default.flush_reward_events", soft_time_limit=8 * 60, time_limit=9 * 60)
def flush_reward_events() -> dict[str, int]:
    """A cada minuto: grava as somas dos eventos e os contatos do buffer, primeiro os lotes que
    sobraram de uma execução anterior."""
    services = get_services()
    totals = {"events": 0, "leads": 0, "skipped": 0}
    if services.redis is None:
        return totals
    with services.lock("reward-events", timeout=LOCK_FOR) as acquired:
        if not acquired:
            return totals
        client = services.redis
        leftovers = [key.decode() for key in client.scan_iter(PROCESSING.format(batch="*"))]
        if client.exists(BUFFER):
            fresh = PROCESSING.format(batch=uuid.uuid4().hex)
            client.rename(BUFFER, fresh)
            leftovers.append(fresh)
        for key in leftovers:
            for name, count in _flush(services, key).items():
                totals[name] += count
    if any(totals.values()):
        log.info("eventos de reward gravados", extra=totals)
    return totals


@app.task(name="avant.default.purge_reward_batches")
def purge_reward_batches_task() -> int:
    """Uma vez por dia: apaga os identificadores de lote com mais de 7 dias (nenhum lote tão
    antigo volta do buffer). Roda sem RLS: a tabela não é de Empresa."""
    services = get_services()
    before = services.clock.now() - KEEP_BATCHES
    return purge_reward_batches(services.trusted_uow(), before=before)


def forget_latest_reward_pages(services: Services, network_id: uuid.UUID) -> int:
    """Depois de importar o inventário da network: apaga o cache das páginas cujo reward usa os
    ad units mais recentes. Falhar aqui não falha a importação (o cache expira em 1 hora)."""
    if services.redis is None:
        return 0
    try:
        pages = latest_reward_pages(services.trusted_uow(), network_id=network_id)
        keys = [PAGE.format(domain=domain, path=path) for domain, path in pages]
        return cast(int, services.redis.delete(*keys)) if keys else 0
    except Exception:
        log.exception("cache dos rewards não foi apagado", extra={"network_id": str(network_id)})
        return 0


def _flush(services: Services, key: str) -> dict[str, int]:
    """Grava a lista da chave em pedaços e apaga a chave no fim."""
    assert services.redis is not None
    totals = {"events": 0, "leads": 0, "skipped": 0}
    batch_id = key.rsplit(":", 1)[-1]
    raw = cast(list[bytes], services.redis.lrange(key, 0, -1))
    for start in range(0, len(raw), CHUNK):
        batch, broken = _batch(f"{batch_id}:{start}", raw[start : start + CHUNK])
        result = record_reward_batch(services.trusted_uow(), batch=batch, clock=services.clock)
        totals["events"] += result.events
        totals["leads"] += result.leads
        totals["skipped"] += result.skipped + broken
    services.redis.delete(key)
    return totals


def _batch(batch_id: str, raw: list[bytes]) -> tuple[RewardBatch, int]:
    """O lote com os itens que estão no formato e quantos não estavam."""
    events: list[RewardEvent] = []
    leads: list[RewardLeadSubmission] = []
    broken = 0
    for item in raw:
        try:
            data = json.loads(item)
            if data.get("type") == "lead":
                leads.append(_lead(data))
            else:
                events.append(_event(data))
        except (ValueError, KeyError, TypeError, AttributeError):
            broken += 1
    return RewardBatch(batch_id, tuple(events), tuple(leads)), broken


def _event(data: dict[str, Any]) -> RewardEvent:
    """O evento do JSON que a api guardou."""
    question = data.get("question_id")
    return RewardEvent(
        reward_id=uuid.UUID(data["reward_id"]),
        day=date.fromisoformat(data["day"]),
        kind=RewardEventKind(data["kind"]),
        step=data.get("step"),
        question_id=uuid.UUID(question) if question else None,
        answer=data.get("answer"),
    )


def _lead(data: dict[str, Any]) -> RewardLeadSubmission:
    """O contato do JSON que a api guardou."""
    return RewardLeadSubmission(
        reward_id=uuid.UUID(data["reward_id"]),
        name=str(data["name"]),
        contact=str(data["contact"]),
        language=str(data["language"]),
        answers=tuple(
            (uuid.UUID(answer["question_id"]), int(answer["answer"])) for answer in data["answers"]
        ),
        created_at=datetime.fromisoformat(data["created_at"]),
    )
