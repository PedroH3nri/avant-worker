"""Tarefas do MCM na network da Groone (fila ``gam``), com ``trusted_uow``.

- ``discover_mcm``: de hora em hora, lê os child publishers da network da Groone e atualiza
  as networks cadastradas (nada é ligado pelo e-mail, core#289). Para cada network pendente
  com o MCM aprovado, pede o teste e a sincronização; o histórico das métricas sai do teste
  quando ela fica ativa.
- ``sync_contracts``: de hora em hora, depois da descoberta, lê o revshare aprovado de cada
  child publisher Manage Account e troca o contrato da network quando ele muda.
"""

import logging

from avant_core.gam.contracts.services import contract_service
from avant_core.gam.sync.services import sync_service

from avant_worker.app import app
from avant_worker.services import get_services
from avant_worker.tasks.gam.network_tasks import LOCK_SECONDS, RETRY_FOR, sync_network

log = logging.getLogger("avant.worker.gam")


@app.task(
    name="avant.gam.discover_mcm",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def discover_mcm() -> dict[str, int]:
    """trusted_uow: a descoberta percorre as networks de todas as Empresas."""
    services = get_services()
    with services.lock("gam:discover_mcm", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": 1}
        found = sync_service.discover_mcm(
            services.trusted_uow(), gam=services.gam, clock=services.clock, mailer=services.mailer
        )
    for company_id, network_id in found.created:
        sync_network.delay(str(company_id), str(network_id))
    counts = {
        "created": len(found.created),
        "candidates": found.candidates,
        "disconnected": found.disconnected,
        "updated": found.updated,
    }
    log.info(
        "descoberta do MCM",
        extra={
            key if key != "created" else "networks_created": value for key, value in counts.items()
        },
    )
    return counts


@app.task(
    name="avant.gam.sync_contracts",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
)
def sync_contracts() -> dict[str, int]:
    """trusted_uow: o revshare de todas as networks Manage Account vem de uma chamada só."""
    services = get_services()
    with services.lock("gam:sync_contracts", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped_run": 1}
        result = contract_service.sync_contracts(
            services.trusted_uow(), gam=services.gam, clock=services.clock
        )
    counts = {"started": result.started, "unchanged": result.unchanged, "skipped": result.skipped}
    log.info("contratos do MCM", extra=counts)
    return counts
