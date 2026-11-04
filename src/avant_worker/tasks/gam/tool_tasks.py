"""Ferramentas do GAM do painel interno (fila ``gam``).

- ``run_tool``: roda uma execução que a API abriu (configuração completa, setup de
  anúncio, key values ou "Sincronizar agora"), passo a passo, pelo caso de uso
  ``execute_gam_tool`` do avant-core, com as escritas do ``SoapGamWriter``.

Usa ``trusted_uow``: a tabela ``gam_tool_runs`` é do painel interno e o RLS dela só deixa
ler sem a Empresa (bypass). Cada passo grava o andamento e publica ``gam_tool_run.updated``
no canal da Company Groone, que é a Empresa aberta de quem está no painel interno.

Sem retry automático: uma escrita que falhou fica registrada no passo e a pessoa roda de
novo. Uma reentrega (``acks_late``) retoma do passo que parou; todo passo confere o GAM antes
de criar, então nada se duplica. A trava no Redis impede duas cópias rodando juntas.
"""

import logging
import uuid
from typing import Any

from avant_core.gam.tools.models import GamToolRun
from avant_core.gam.tools.services import execute_gam_tool

from avant_worker.adapters.events import GAM_TOOL_RUN_UPDATED, publish
from avant_worker.app import app
from avant_worker.services import GamNotConfigured, Services, get_services
from avant_worker.tasks.gam.network_tasks import sync_network

log = logging.getLogger("avant.worker.gam")

LOCK_SECONDS = 60 * 60


@app.task(name="avant.gam.run_tool")
def run_tool(run_id: str) -> dict[str, Any]:
    """Roda a execução da ferramenta do GAM e avisa o painel a cada passo."""
    services = get_services()
    run_uuid = uuid.UUID(run_id)
    with services.lock(f"gam:tool:{run_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            log.info("execução já rodando", extra={"run_id": run_id})
            return {"skipped": "locked"}
        with services.trusted_uow() as uow:
            pending = uow.gam_tool_runs.get(run_uuid)
            groone = uow.companies.internal()
        if pending is None:
            return {"skipped": "missing"}
        groone_code = services.settings.gam_groone_network_code
        if not groone_code:
            raise GamNotConfigured("defina GAM_GROONE_NETWORK_CODE neste worker")
        company_id = pending.company_id
        groone_id = groone.id if groone is not None else None
        run = execute_gam_tool(
            services.trusted_uow(),
            services.gam_writer,
            run_id=run_uuid,
            groone_network_code=groone_code,
            clock=services.clock,
            notify=lambda current: _updated(services, groone_id, current),
            import_inventory=lambda network_id: _import(company_id, network_id),
        )
    if run is None:
        return {"skipped": "not_running"}
    log.info(
        "ferramenta do GAM terminou",
        extra={"run_id": run_id, "state": run.state.value, "error": run.error_code},
    )
    return {"state": run.state.value, "error": run.error_code}


def _updated(services: Services, groone_id: uuid.UUID | None, run: GamToolRun) -> None:
    """Avisa o painel interno que a execução andou."""
    if groone_id is None:
        return
    publish(
        services.redis,
        groone_id,
        GAM_TOOL_RUN_UPDATED,
        {"run_id": str(run.id), "network_id": str(run.network_id)},
    )


def _import(company_id: uuid.UUID, network_id: uuid.UUID) -> None:
    """Enfileira a importação de sites e blocos da network, com o teste de acesso."""
    sync_network.delay(str(company_id), str(network_id))
