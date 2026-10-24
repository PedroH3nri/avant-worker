"""Avisos para a tela em tempo real: o worker publica no Redis e a API repassa por SSE
(``GET /api/v1/events``) a quem está com a Empresa aberta.

Contrato, igual ao da API: canal ``avant:events:{company_id}``, mensagem JSON
``{"type": "network.updated", "data": {"network_id": "..."}}``. O evento só diz o que
mudou; a tela busca o estado pela rota de sempre, que confere a permissão.
"""

import json
import logging
import uuid

import redis

log = logging.getLogger("avant.worker.events")

NETWORK_UPDATED = "network.updated"
METRICS_UPDATED = "metrics.updated"


def channel(company_id: uuid.UUID) -> str:
    """Nome do canal do Redis com os eventos de uma Empresa."""
    return f"avant:events:{company_id}"


def publish(
    client: "redis.Redis | None", company_id: uuid.UUID, type_: str, data: dict[str, str]
) -> None:
    """Sem Redis (local), não há tela para avisar. Falha ao publicar não derruba a tarefa."""
    if client is None:
        return
    try:
        client.publish(channel(company_id), json.dumps({"type": type_, "data": data}))
    except redis.RedisError:
        log.warning("não foi possível publicar o evento", extra={"type": type_}, exc_info=True)
