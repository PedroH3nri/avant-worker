"""Sincronia com o Google Ads (decisão 17), na fila ``google_ads``.

O agendador lista logins e contas de todas as Empresas com ``trusted_uow()`` (só para varrer) e
manda uma tarefa por login ou conta, que roda no Unit of Work da Empresa (RLS). Erro temporário
do Google (cota, 5xx, rede) tenta de novo em 1, 2, 4 e 8 minutos; token revogado não é erro da
tarefa: o core marca o login e avisa quem conectou. Cada consulta é um ``searchStream`` por
conta, para poupar a cota do developer token.

G2: depois de cada sincronia de números, a conta passa pelos limites de gasto; a sincronia
noturna dos termos também confere os termos que gastam sem retorno. As regras automáticas rodam
uma vez por dia, às 06:20 de São Paulo, depois dos números do dia anterior.

G3: a api grava o job de criar ou editar e manda ``run_job``; o core faz a chamada e o começo e
o fim viram o evento ``google_ads.job.updated`` para a tela acompanhar.
"""

import logging
import uuid
from typing import Any

from avant_core.google_ads.enums import GoogleAdsJobKind, GoogleAdsJobState
from avant_core.google_ads.errors import GoogleAdsUnavailable
from avant_core.google_ads.models import GoogleAdsJob
from avant_core.google_ads.services import (
    enforce_google_ads_limits,
    execute_google_ads_job,
    google_ads_accounts_to_sync,
    google_ads_logins_to_sync,
    google_ads_rule_accounts,
    run_google_ads_rules,
    sync_google_ads_changes,
    sync_google_ads_login,
    sync_google_ads_metrics,
    warn_google_ads_bad_terms,
)

from avant_worker.adapters.events import GOOGLE_ADS_JOB_UPDATED, publish
from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.google_ads")

LOCK_SECONDS = 15 * 60
JOB_SOFT_LIMIT_SECONDS = 5 * 60
JOB_HARD_LIMIT_SECONDS = 6 * 60
JOB_LOCK_SECONDS = JOB_HARD_LIMIT_SECONDS + 60
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
    """Grava os números dos últimos ``days`` dias (com ``with_terms``, termos, posicionamentos e
    o aviso de termos ruins) e confere os limites de gasto da conta."""
    services = get_services()
    with services.lock(f"google_ads:metrics:{account_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        rows = sync_google_ads_metrics(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            account_id=uuid.UUID(account_id),
            days=days,
            clock=services.clock,
            with_terms=with_terms,
        )
        changed = enforce_google_ads_limits(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            account_id=uuid.UUID(account_id),
            clock=services.clock,
        )
        bad_terms = (
            warn_google_ads_bad_terms(
                services.uow(uuid.UUID(company_id)),
                account_id=uuid.UUID(account_id),
                clock=services.clock,
            )
            if with_terms
            else 0
        )
    if changed or bad_terms:
        log.info(
            "limite ou termos do google ads",
            extra={"account_id": account_id, "changed": changed, "bad_terms": bad_terms},
        )
    return rows


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


@app.task(name="avant.google_ads.schedule_rules", soft_time_limit=5 * 60, time_limit=6 * 60)
def schedule_rules() -> int:
    """Todo dia às 09:20 UTC (06:20 em São Paulo), depois da sincronia de ontem das 08:45: uma
    tarefa por conta com regra ligada. Varre todas as Empresas com ``trusted_uow()``."""
    targets = google_ads_rule_accounts(get_services().trusted_uow())
    for target in targets:
        run_rules.delay(str(target.company_id), str(target.target_id))
    return len(targets)


@app.task(
    name="avant.google_ads.run_rules",
    autoretry_for=RETRY_FOR,
    retry_backoff=60,
    retry_backoff_max=8 * 60,
    retry_jitter=False,
    max_retries=4,
    soft_time_limit=12 * 60,
    time_limit=14 * 60,
)
def run_rules(company_id: str, account_id: str) -> int:
    """Escala o orçamento e o CPC e pausa pelo ROI de ontem; o core não repete a decisão do
    mesmo dia."""
    services = get_services()
    with services.lock(f"google_ads:rules:{account_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        return run_google_ads_rules(
            services.uow(uuid.UUID(company_id)),
            gateway=services.google_ads,
            box=services.google_ads_box,
            account_id=uuid.UUID(account_id),
            clock=services.clock,
        )


@app.task(
    name="avant.google_ads.run_job",
    bind=True,
    soft_time_limit=JOB_SOFT_LIMIT_SECONDS,
    time_limit=JOB_HARD_LIMIT_SECONDS,
    max_retries=1,
)
def run_job(self: Any, company_id: str, job_id: str) -> str:
    """Cria a campanha ou edita o nível pelo job; rodar de novo não chama o Google outra vez.
    Trava ocupada (talvez de um worker que caiu) tenta de novo depois que ela vence."""
    services = get_services()
    company_uuid = uuid.UUID(company_id)

    def notify(job: GoogleAdsJob) -> None:
        """Avisa a tela aberta que o job mudou de situação."""
        publish(services.redis, company_uuid, GOOGLE_ADS_JOB_UPDATED, {"job_id": str(job.id)})

    with services.lock(f"google_ads:job:{job_id}", timeout=JOB_LOCK_SECONDS) as locked:
        if not locked:
            raise self.retry(countdown=JOB_LOCK_SECONDS)
        job = execute_google_ads_job(
            services.uow(company_uuid),
            gateway=services.google_ads,
            box=services.google_ads_box,
            job_id=uuid.UUID(job_id),
            clock=services.clock,
            notify=notify,
        )
    if job is None:
        return "skipped"
    if job.kind is GoogleAdsJobKind.CREATE and job.state is GoogleAdsJobState.DONE:
        _sync_created(company_uuid, job.account_id)
    log.info(
        "job do google ads terminado",
        extra={"job_id": job_id, "state": job.state.value, "error": job.error_code},
    )
    return job.state.value


def _sync_created(company_id: uuid.UUID, account_id: uuid.UUID) -> None:
    """Pede a sincronia do login da conta, que traz a campanha que acabou de nascer."""
    with get_services().uow(company_id) as uow:
        account = uow.google_ads_accounts.get(account_id)
        login_id = account.login_id if account else None
    if login_id is not None:
        sync_login.delay(str(company_id), str(login_id))
