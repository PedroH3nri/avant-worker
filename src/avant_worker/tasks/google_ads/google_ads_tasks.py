"""Sincronia com o Google Ads (decisão 17), na fila ``google_ads``.

O agendador lista logins e contas de todas as Empresas com ``trusted_uow()`` (só para varrer) e
manda uma tarefa por login ou conta, que roda no Unit of Work da Empresa (RLS). Erro temporário
do Google (cota, 5xx, rede) tenta de novo em 1, 2, 4 e 8 minutos; token revogado não é erro da
tarefa: o core marca o login e avisa quem conectou. Cada consulta é um ``searchStream`` por
conta, para poupar a cota do developer token.
"""

import logging
import uuid
from typing import Any

from avant_core.google_ads.errors import GoogleAdsUnavailable
from avant_core.google_ads.services import (
    google_ads_accounts_to_sync,
    google_ads_logins_to_sync,
    sync_google_ads_changes,
    sync_google_ads_login,
    sync_google_ads_metrics,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.google_ads")

LOCK_SECONDS = 15 * 60
RETRY_FOR = (GoogleAdsUnavailable,)
TODAY = 1
LATE_DAYS = 3


@app.task(name="avant.google_ads.schedule_structure", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_structure() -> int:
    """De hora em hora (:35): uma sincronia de contas e estrutura por login com token. Varre
    todas as Empresas com ``trusted_uow()``."""
    targets = google_ads_logins_to_sync(get_services().trusted_uow())
    for target in targets:
        sync_login.delay(str(target.company_id), str(target.target_id))
    return len(targets)


@app.task(
    name="avant.google_ads.sync_login",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def sync_login(company_id: str, login_id: str) -> dict[str, Any]:
    """Traz as contas do login (as novas da MCC também) e as campanhas, grupos, anúncios e
    palavras-chave de cada conta ativa."""
    services = get_services()
    with services.lock(f"google_ads:login:{login_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": "locked"}
        result = sync_google_ads_login(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            login_id=uuid.UUID(login_id),
            clock=services.clock,
        )
    summary = {
        "accounts": result.accounts,
        "objects": result.objects,
        "keywords": result.keywords,
        "alerts": result.alerts,
        "error": result.error,
    }
    log.info("login do google ads sincronizado", extra={"login_id": login_id, **summary})
    return summary


@app.task(name="avant.google_ads.schedule_metrics", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_metrics(days: int = TODAY, with_terms: bool = False) -> int:
    """A cada 30 minutos (:05 e :35) os números de hoje; às 02:40 os últimos 3 dias com termos e
    posicionamentos. Varre todas as Empresas com ``trusted_uow()``."""
    targets = google_ads_accounts_to_sync(get_services().trusted_uow())
    for target in targets:
        sync_metrics.delay(str(target.company_id), str(target.target_id), days, with_terms)
    return len(targets)


@app.task(
    name="avant.google_ads.sync_metrics",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def sync_metrics(
    company_id: str, account_id: str, days: int = TODAY, with_terms: bool = False
) -> int:
    """Grava os números por campanha, anúncio e palavra-chave dos últimos ``days`` dias e, com
    ``with_terms``, por termo de pesquisa e posicionamento."""
    services = get_services()
    with services.lock(f"google_ads:metrics:{account_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        return sync_google_ads_metrics(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            account_id=uuid.UUID(account_id),
            days=days,
            clock=services.clock,
            with_terms=with_terms,
        )


@app.task(name="avant.google_ads.schedule_changes", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_changes() -> int:
    """De hora em hora (:37): o histórico do ``change_event`` de cada conta ativa. Varre todas
    as Empresas com ``trusted_uow()``."""
    targets = google_ads_accounts_to_sync(get_services().trusted_uow())
    for target in targets:
        sync_changes.delay(str(target.company_id), str(target.target_id))
    return len(targets)


@app.task(
    name="avant.google_ads.sync_changes",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def sync_changes(company_id: str, account_id: str) -> int:
    """Grava no histórico o que mudou direto no Google Ads desde a última vez."""
    services = get_services()
    with services.lock(f"google_ads:changes:{account_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        return sync_google_ads_changes(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            account_id=uuid.UUID(account_id),
            clock=services.clock,
        )
