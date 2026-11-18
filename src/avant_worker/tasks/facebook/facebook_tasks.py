"""Sincronia com o Facebook (decisão 16), na fila ``facebook``.

O agendador lista perfis e contas de todas as Empresas com ``trusted_uow()`` (só para
varrer) e manda uma tarefa por perfil ou conta, que roda no Unit of Work da Empresa (RLS).
Erro temporário do Facebook (limite de chamadas, 5xx, rede) tenta de novo em 1, 2, 4 e 8
minutos; token inválido não é erro da tarefa: o core marca o perfil e avisa quem conectou.
"""

import logging
import uuid
from typing import Any

from avant_core.facebook.errors import FacebookUnavailable
from avant_core.facebook.services import (
    check_facebook_tokens,
    facebook_accounts_to_sync,
    facebook_profiles_to_sync,
    sync_facebook_insights,
    sync_facebook_profile,
)

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.facebook")

LOCK_SECONDS = 15 * 60
RETRY_FOR = (FacebookUnavailable,)
TODAY = 1
LATE_DAYS = 3


@app.task(name="avant.facebook.schedule_structure", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_structure() -> int:
    """De hora em hora (:25): uma sincronia de contas e estrutura por perfil com token. Varre
    todas as Empresas com ``trusted_uow()``."""
    targets = facebook_profiles_to_sync(get_services().trusted_uow())
    for target in targets:
        sync_profile.delay(str(target.company_id), str(target.target_id))
    return len(targets)


@app.task(
    name="avant.facebook.sync_profile",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def sync_profile(company_id: str, profile_id: str) -> dict[str, Any]:
    """Traz as contas do perfil e o que mudou nas campanhas, conjuntos e anúncios."""
    services = get_services()
    with services.lock(f"facebook:profile:{profile_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return {"skipped": "locked"}
        result = sync_facebook_profile(
            services.uow(uuid.UUID(company_id)),
            gateway=services.facebook,
            box=services.facebook_box,
            profile_id=uuid.UUID(profile_id),
            clock=services.clock,
        )
    summary = {
        "accounts": result.accounts,
        "objects": result.objects,
        "changes": result.changes,
        "alerts": result.alerts,
        "error": result.error,
    }
    log.info("perfil do facebook sincronizado", extra={"profile_id": profile_id, **summary})
    return summary


@app.task(name="avant.facebook.schedule_insights", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_insights(days: int = TODAY) -> int:
    """A cada 30 minutos (:15 e :45) os números de hoje; às 02:30 os últimos 3 dias, que o
    Facebook ainda ajusta. Varre todas as Empresas com ``trusted_uow()``."""
    targets = facebook_accounts_to_sync(get_services().trusted_uow())
    for target in targets:
        sync_insights.delay(str(target.company_id), str(target.target_id), days)
    return len(targets)


@app.task(
    name="avant.facebook.sync_insights",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def sync_insights(company_id: str, account_id: str, days: int = TODAY) -> int:
    """Grava os números por anúncio e por conjunto e país dos últimos ``days`` dias."""
    services = get_services()
    with services.lock(f"facebook:insights:{account_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        return sync_facebook_insights(
            services.uow(uuid.UUID(company_id)),
            gateway=services.facebook,
            box=services.facebook_box,
            account_id=uuid.UUID(account_id),
            days=days,
            clock=services.clock,
        )


@app.task(name="avant.facebook.check_tokens", soft_time_limit=5 * 60, time_limit=6 * 60)
def check_tokens() -> int:
    """Todo dia às 08:00: avisa quem conectou um perfil cujo token vence em até 7 dias. Varre
    todas as Empresas com ``trusted_uow()``."""
    services = get_services()
    return check_facebook_tokens(services.trusted_uow(), clock=services.clock)
