"""Tarefas da miniatura guardada dos relatórios salvos (fila ``default``).

- ``refresh_report_preview``: a API pede ao criar, editar ou duplicar um relatório.
- ``refresh_report_previews``: de hora em hora (depois das métricas do GAM), refaz as miniaturas
  que faltam ou têm mais de 1 hora, até ``BATCH`` por vez.

As duas usam ``trusted_uow``: a miniatura soma todos os sites da Empresa, e a lista das velhas
olha todas as Empresas. Refazer de novo só troca a miniatura pela mais nova.
"""

import logging
import uuid

from avant_core.reports.services import refresh_preview, stale_report_ids

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.reports")

BATCH = 500
LOCK_SECONDS = 1800


@app.task(name="avant.default.refresh_report_preview")
def refresh_report_preview(report_id: str) -> dict[str, int]:
    """trusted_uow: refaz a miniatura de um relatório; o que sumiu não conta."""
    services = get_services()
    found = refresh_preview(
        services.trusted_uow(), report_id=uuid.UUID(report_id), clock=services.clock
    )
    return {"refreshed": int(found)}


@app.task(name="avant.default.refresh_report_previews")
def refresh_report_previews() -> dict[str, int]:
    """trusted_uow: refaz as miniaturas que faltam ou estão velhas, uma por vez."""
    services = get_services()
    with services.lock("report-previews", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        ids = stale_report_ids(services.trusted_uow(), clock=services.clock, limit=BATCH)
        refreshed = 0
        for report_id in ids:
            try:
                refreshed += int(
                    refresh_preview(
                        services.trusted_uow(), report_id=report_id, clock=services.clock
                    )
                )
            except Exception:
                log.exception("miniatura do relatório falhou", extra={"report_id": str(report_id)})
    log.info("miniaturas refeitas", extra={"stale": len(ids), "refreshed": refreshed})
    return {"stale": len(ids), "refreshed": refreshed}
