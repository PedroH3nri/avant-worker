"""Tarefas da verificação de instalação da ad tag, do loader e do reward (decisão 21).

- ``check_install``: verifica um item pedido no botão do painel, com ``services.uow`` da
  Empresa (RLS). O ``trusted_uow`` só conta quantas Empresas têm o domínio do reward ativo.
- ``daily_install_checks``: todo dia às 06:30 UTC (03:30 em Brasília) lista, com
  ``trusted_uow`` (varre todas as Empresas), as ad tags publicadas, os loaders em uso e os
  rewards ativos, e pede a verificação de cada site pelo ``dispatch_install_checks``.
- ``dispatch_install_checks``: solta 12 sites por minuto e se reagenda com o resto, como o
  checklist.
- ``check_site_installs``: verifica os itens de um site com uma busca só por página e grava
  com "rotina" no lugar de quem pediu.

Cada verificação avisa a tela pelo evento ``install_check.updated``. Rodar de novo só verifica
outra vez.
"""

import logging
import uuid
from itertools import groupby
from typing import Any

from avant_core.install_checks.enums import InstallCheckSource, InstallTarget
from avant_core.install_checks.models import InstallCheck
from avant_core.install_checks.services import (
    MemoFetcher,
    daily_install_targets,
    run_install_check,
)
from avant_core.site_checklists.interfaces import PageFetcher

from avant_worker.adapters.events import INSTALL_CHECK_UPDATED, publish
from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.install_checks")

LOCK_SECONDS = 5 * 60
SOFT_LIMIT_SECONDS = 4 * 60
HARD_LIMIT_SECONDS = 4 * 60 + 30
SITES_PER_BATCH = 12
BATCH_SECONDS = 60


@app.task(
    name="avant.default.check_install",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def check_install(company_id: str, target: str, target_id: str) -> dict[str, int]:
    """Verifica o item pedido no botão e avisa a tela."""
    services = get_services()
    with services.lock(f"install_check:{target}:{target_id}", timeout=LOCK_SECONDS) as acquired:
        if not acquired:
            return {"skipped": 1}
        check = _run(
            services,
            uuid.UUID(company_id),
            InstallTarget(target),
            uuid.UUID(target_id),
            services.page_fetcher,
            InstallCheckSource.MANUAL,
        )
    log.info("instalação verificada", extra={"target": target, "target_id": target_id})
    return {"checked": int(check is not None)}


@app.task(
    name="avant.default.daily_install_checks",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def daily_install_checks() -> dict[str, int]:
    """trusted_uow: lista o que a rotina verifica e pede a verificação de cada site."""
    services = get_services()
    targets = daily_install_targets(services.trusted_uow())
    sites: list[list[Any]] = [
        [str(company_id), [[item.target.value, str(item.target_id)] for item in items]]
        for (company_id, _site_id), items in groupby(
            targets, key=lambda item: (item.company_id, item.site_id)
        )
    ]
    _dispatch(sites)
    log.info("rotina de instalação", extra={"sites": len(sites), "items": len(targets)})
    return {"sites": len(sites), "items": len(targets)}


@app.task(
    name="avant.default.dispatch_install_checks",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def dispatch_install_checks(sites: list[list[Any]]) -> int:
    """Solta o próximo lote de sites e agenda o resto para daqui a um minuto."""
    return _dispatch(sites)


@app.task(
    name="avant.default.check_site_installs",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def check_site_installs(company_id: str, items: list[list[str]]) -> dict[str, int]:
    """Verifica os itens de um site na rotina, sem buscar a mesma página duas vezes."""
    services = get_services()
    fetcher = MemoFetcher(services.page_fetcher)
    checked = 0
    for target, target_id in items:
        with services.lock(f"install_check:{target}:{target_id}", timeout=LOCK_SECONDS) as acquired:
            if not acquired:
                continue
            check = _run(
                services,
                uuid.UUID(company_id),
                InstallTarget(target),
                uuid.UUID(target_id),
                fetcher,
                InstallCheckSource.DAILY,
            )
            checked += int(check is not None)
    return {"checked": checked}


def _dispatch(sites: list[list[Any]]) -> int:
    """Pede a verificação dos primeiros sites, espaçadas no minuto; devolve quantos."""
    batch, rest = sites[:SITES_PER_BATCH], sites[SITES_PER_BATCH:]
    spacing = BATCH_SECONDS // SITES_PER_BATCH
    for index, (company_id, items) in enumerate(batch):
        check_site_installs.apply_async(args=(company_id, items), countdown=index * spacing)
    if rest:
        dispatch_install_checks.apply_async(args=(rest,), countdown=BATCH_SECONDS)
    return len(batch)


def _run(
    services: Services,
    company_id: uuid.UUID,
    target: InstallTarget,
    target_id: uuid.UUID,
    fetcher: PageFetcher,
    source: InstallCheckSource,
) -> InstallCheck | None:
    """Verifica com o RLS da Empresa, grava e avisa a tela."""
    check = run_install_check(
        services.uow(company_id),
        target=target,
        target_id=target_id,
        fetcher=fetcher,
        source=source,
        clock=services.clock,
        trusted=services.trusted_uow(),
    )
    if check is not None:
        publish(
            services.redis,
            company_id,
            INSTALL_CHECK_UPDATED,
            {"target": target.value, "target_id": str(target_id)},
        )
    return check
