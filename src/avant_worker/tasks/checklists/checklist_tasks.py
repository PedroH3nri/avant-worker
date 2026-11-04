"""Tarefas do checklist de domínio automatizado.

- ``open_checklists``: todo dia às 03:15, abre o checklist do mês dos sites que faturaram no
  mês anterior (no dia 1 cria; nos outros dias só pega o que ficou sem conferir) e pede a
  conferência de cada um pelo ``dispatch_checklists``.
- ``dispatch_checklists``: solta 12 conferências por minuto, espaçadas em menos de um minuto,
  e se reagenda com o resto. Sem ETA longa (o RabbitMQ devolve a mensagem que fica 30 minutos
  sem ack) e sem ``rate_limit``, que segura as mensagens no worker e trava a fila ``default``.
- ``check_checklist``: confere um site (página inicial, um artigo e o ads.txt) e grava. O
  painel pede esta tarefa no "Conferir agora".

As duas usam ``trusted_uow``: as tabelas do checklist são só do painel interno e o RLS delas
só deixa ler com bypass. Rodar de novo só confere outra vez.
"""

import logging
import uuid

from avant_core.site_checklists.services import check_site, open_checklist_month

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.checklists")

LOCK_SECONDS = 5 * 60
# Abaixo da trava de 5 minutos.
SOFT_LIMIT_SECONDS = 4 * 60
HARD_LIMIT_SECONDS = 4 * 60 + 30
CHECKS_PER_BATCH = 12
BATCH_SECONDS = 60


@app.task(
    name="avant.default.open_checklists",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def open_checklists() -> dict[str, int]:
    """trusted_uow: abre o mês e pede a conferência dos checklists ainda não conferidos."""
    services = get_services()
    checklist_ids = open_checklist_month(services.trusted_uow(), clock=services.clock)
    _dispatch([str(checklist_id) for checklist_id in checklist_ids])
    log.info("checklists abertos", extra={"to_check": len(checklist_ids)})
    return {"to_check": len(checklist_ids)}


@app.task(
    name="avant.default.dispatch_checklists",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def dispatch_checklists(checklist_ids: list[str]) -> int:
    """Solta o próximo lote de conferências e agenda o resto para daqui a um minuto."""
    return _dispatch(checklist_ids)


def _dispatch(checklist_ids: list[str]) -> int:
    """Pede a conferência dos primeiros checklists, espaçadas no minuto; devolve quantos."""
    batch, rest = checklist_ids[:CHECKS_PER_BATCH], checklist_ids[CHECKS_PER_BATCH:]
    spacing = BATCH_SECONDS // CHECKS_PER_BATCH
    for index, checklist_id in enumerate(batch):
        check_checklist.apply_async(args=(checklist_id,), countdown=index * spacing)
    if rest:
        dispatch_checklists.apply_async(args=(rest,), countdown=BATCH_SECONDS)
    return len(batch)


@app.task(
    name="avant.default.check_checklist",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def check_checklist(checklist_id: str) -> dict[str, int]:
    """trusted_uow: confere o site do checklist e grava o resultado de cada item."""
    services = get_services()
    with services.lock(f"checklist:{checklist_id}", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        checked = check_site(
            services.trusted_uow(),
            checklist_id=uuid.UUID(checklist_id),
            fetcher=services.page_fetcher,
            clock=services.clock,
        )
    log.info("checklist conferido", extra={"checklist_id": checklist_id, "checked": checked})
    return {"checked": int(checked)}
