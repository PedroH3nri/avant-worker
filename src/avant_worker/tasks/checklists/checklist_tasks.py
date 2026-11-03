"""Tarefas do checklist de domínio automatizado.

- ``open_checklists``: todo dia às 03:15, abre o checklist do mês dos sites que faturaram no
  mês anterior (no dia 1 cria; nos outros dias só pega o que ficou sem conferir) e pede a
  conferência de cada um, espaçadas.
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
SPACING_SECONDS = 5


@app.task(name="avant.default.open_checklists")
def open_checklists() -> dict[str, int]:
    """trusted_uow: abre o mês e pede a conferência dos checklists ainda não conferidos."""
    services = get_services()
    checklist_ids = open_checklist_month(services.trusted_uow(), clock=services.clock)
    for index, checklist_id in enumerate(checklist_ids):
        check_checklist.apply_async(args=(str(checklist_id),), countdown=index * SPACING_SECONDS)
    log.info("checklists abertos", extra={"to_check": len(checklist_ids)})
    return {"to_check": len(checklist_ids)}


@app.task(name="avant.default.check_checklist")
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
