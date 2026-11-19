"""Facebook: o agendador manda uma tarefa por perfil e por conta, que grava estrutura e
números na Empresa; erro temporário tenta de novo e worker sem o app falha claro."""

import uuid
from collections import defaultdict
from datetime import date, datetime
from typing import Any

import pytest
from avant_core.facebook.enums import (
    FacebookAccountState,
    FacebookJobKind,
    FacebookJobState,
    FacebookLevel,
    FacebookListKind,
    FacebookOnLimit,
)
from avant_core.facebook.errors import FacebookUnavailable
from avant_core.facebook.models import (
    FacebookAccountData,
    FacebookCountryRow,
    FacebookDraft,
    FacebookDraftAd,
    FacebookDraftAdset,
    FacebookInsightRow,
    FacebookJob,
    FacebookObjectData,
    FacebookOption,
    FacebookProfile,
    FacebookToken,
)
from avant_core.identity.security.crypto import FernetSecretBox
from celery.exceptions import Retry
from cryptography.fernet import Fernet
from sqlalchemy import text

from avant_worker.app import _route, app
from avant_worker.services import FacebookNotConfigured, Services
from avant_worker.tasks.facebook import (
    check_tokens,
    email_alerts,
    run_job,
    run_rules,
    schedule_insights,
    schedule_rules,
    schedule_structure,
    sync_insights,
    sync_profile,
)
from tests.test_gam_tasks import company

ACCOUNT = "act_123"


class FakeFacebook:
    """A Graph API com uma conta, uma campanha com um conjunto e um anúncio e os números."""

    def __init__(self) -> None:
        self.unavailable = False
        self.calls: defaultdict[str, int] = defaultdict(int)
        self.statuses: list[tuple[str, str]] = []

    def exchange_code(self, code: str, redirect_uri: str) -> FacebookToken:
        """Não usado pelo worker."""
        raise NotImplementedError

    def ad_accounts(self, token: str) -> list[FacebookAccountData]:
        """A conta de teste, ou o erro temporário."""
        self.calls["ad_accounts"] += 1
        if self.unavailable:
            raise FacebookUnavailable("limite de chamadas")
        return [
            FacebookAccountData(
                ACCOUNT,
                "Conta",
                "bm-1",
                "BM",
                "BRL",
                "America/Sao_Paulo",
                FacebookAccountState.ACTIVE,
            )
        ]

    def objects(
        self, token: str, account_external_id: str, currency: str, since: datetime | None
    ) -> list[FacebookObjectData]:
        """Campanha, conjunto e anúncio."""
        return [
            FacebookObjectData(
                FacebookLevel.CAMPAIGN, "c1", "Campanha", None, "c1", "ACTIVE", "ACTIVE", None
            ),
            FacebookObjectData(
                FacebookLevel.ADSET, "s1", "Conjunto", "c1", "c1", "ACTIVE", "ACTIVE", None
            ),
            FacebookObjectData(
                FacebookLevel.AD, "a1", "Anúncio", "s1", "c1", "ACTIVE", "ACTIVE", None
            ),
        ]

    def insights(
        self, token: str, account_external_id: str, since: date, until: date
    ) -> list[FacebookInsightRow]:
        """Uma linha por dia do período."""
        self.calls["insights"] += 1
        return [FacebookInsightRow("a1", "s1", "c1", until, 5_000_000, 1000, 800, 30, 20, 15)]

    def country_insights(
        self, token: str, account_external_id: str, since: date, until: date
    ) -> list[FacebookCountryRow]:
        """Sem números por país."""
        return []

    def revoke(self, token: str) -> None:
        """Não usado pelo worker."""

    def set_status(self, token: str, external_id: str, status: str) -> None:
        """Guarda a troca de situação feita pelo limite ou pelas regras."""
        self.statuses.append((external_id, status))

    def set_budget(
        self,
        token: str,
        external_id: str,
        currency: str,
        *,
        daily_budget_micros: int | None,
        lifetime_budget_micros: int | None,
    ) -> None:
        """Não usado neste teste."""

    def copy(self, token: str, external_id: str, level: FacebookLevel, *, paused: bool) -> str:
        """Guarda a cópia e devolve o id novo."""
        self.calls["copy"] += 1
        return f"{external_id}-copia"

    def options(
        self, token: str, account_external_id: str, kind: FacebookListKind, query: str
    ) -> list[FacebookOption]:
        """Não usado pelo worker."""
        return []

    def upload_image(
        self, token: str, account_external_id: str, filename: str, content: bytes
    ) -> str:
        """Não usado pelo worker."""
        return "hash-1"

    def upload_video(
        self, token: str, account_external_id: str, filename: str, content: bytes
    ) -> str:
        """Não usado pelo worker."""
        return "video-1"

    def create_campaign(
        self, token: str, account_external_id: str, currency: str, draft: FacebookDraft
    ) -> str:
        """Não usado neste teste."""
        return "campaign-1"

    def create_adset(
        self,
        token: str,
        account_external_id: str,
        currency: str,
        draft: FacebookDraft,
        adset: FacebookDraftAdset,
        campaign_id: str,
    ) -> str:
        """Não usado neste teste."""
        return "adset-1"

    def create_creative(
        self, token: str, account_external_id: str, ad: FacebookDraftAd, link: str
    ) -> str:
        """Não usado neste teste."""
        return "creative-1"

    def create_ad(
        self, token: str, account_external_id: str, name: str, adset_id: str, creative_id: str
    ) -> str:
        """Não usado neste teste."""
        return "ad-1"

    def update_object(
        self,
        token: str,
        external_id: str,
        currency: str,
        *,
        name: str | None,
        spend_cap_micros: int | None,
    ) -> None:
        """Não usado neste teste."""

    def update_adset(self, token: str, external_id: str, adset: FacebookDraftAdset) -> None:
        """Não usado neste teste."""

    def set_creative(self, token: str, ad_external_id: str, creative_id: str) -> None:
        """Não usado neste teste."""


@pytest.fixture
def facebook(services: Services) -> FakeFacebook:
    """Os serviços com a Graph API falsa e uma chave de tokens nova."""
    fake = FakeFacebook()
    services._facebook = fake
    services._facebook_box = FernetSecretBox(Fernet.generate_key().decode())
    return fake


def _profile(services: Services) -> tuple[uuid.UUID, FacebookProfile]:
    """Uma Empresa com um perfil do Facebook conectado."""
    owner = company(services, email=f"dono-{uuid.uuid4().hex[:6]}@blog.com")
    profile = FacebookProfile(
        company_id=owner.id,
        user_id=owner.owner_user_id,
        facebook_user_id="fb-1",
        name="Pedro",
        token_ciphertext=services.facebook_box.encrypt("token-1"),
        token_expires_at=None,
        connected_at=services.clock.now(),
    )
    with services.uow(owner.id) as uow:
        uow.facebook_profiles.add(profile)
        uow.commit()
    return owner.id, profile


def _count(services: Services, table: str) -> int:
    """Quantas linhas a tabela tem, sem RLS."""
    with services.trusted_uow() as uow:
        return int(uow.session.execute(text(f"SELECT count(*) FROM {table}")).scalar_one())


def test_tasks_go_to_the_facebook_queue_and_retry_on_unavailable() -> None:
    for name in (
        "avant.facebook.schedule_structure",
        "avant.facebook.sync_profile",
        "avant.facebook.schedule_insights",
        "avant.facebook.sync_insights",
        "avant.facebook.check_tokens",
        "avant.facebook.schedule_rules",
        "avant.facebook.run_rules",
    ):
        assert name in app.tasks
        assert _route(name) == {"queue": "facebook"}
    assert _route("avant.mail.facebook_alerts") == {"queue": "mail"}
    for task in (sync_profile, sync_insights, run_rules):
        typed: Any = task
        assert typed.autoretry_for == (FacebookUnavailable,) and typed.max_retries == 4


def test_beat_runs_structure_hourly_and_insights_every_thirty_minutes() -> None:
    schedule = app.conf.beat_schedule
    assert schedule["facebook-structure"]["task"] == "avant.facebook.schedule_structure"
    assert schedule["facebook-insights-today"]["schedule"].minute == {15, 45}
    assert schedule["facebook-insights-late"]["kwargs"] == {"days": 3}
    assert schedule["facebook-tokens"]["task"] == "avant.facebook.check_tokens"
    assert schedule["facebook-rules"]["schedule"].hour == {9}
    assert schedule["facebook-alert-mails"]["task"] == "avant.mail.facebook_alerts"


def test_structure_then_insights_fill_the_company(
    services: Services, facebook: FakeFacebook
) -> None:
    _profile(services)
    assert schedule_structure.delay().get() == 1
    assert _count(services, "facebook_ad_accounts") == 1
    assert _count(services, "facebook_objects") == 3
    assert schedule_insights.delay().get() == 1
    assert _count(services, "metrics.facebook_insights_daily") == 1
    assert schedule_insights.delay(3).get() == 1
    assert _count(services, "metrics.facebook_insights_daily") == 1


def test_sync_profile_is_idempotent(services: Services, facebook: FakeFacebook) -> None:
    company_id, profile = _profile(services)
    sync_profile.delay(str(company_id), str(profile.id)).get()
    second = sync_profile.delay(str(company_id), str(profile.id)).get()
    assert _count(services, "facebook_objects") == 3
    assert second["changes"] == 0 and second["error"] is None


def test_unavailable_is_retried(services: Services, facebook: FakeFacebook) -> None:
    company_id, profile = _profile(services)
    facebook.unavailable = True
    with pytest.raises(Retry):
        sync_profile.apply(args=(str(company_id), str(profile.id)), throw=True)
    with pytest.raises(FacebookUnavailable):
        sync_profile._orig_run(str(company_id), str(profile.id))  # type: ignore[attr-defined]


def test_check_tokens_runs_without_profiles(services: Services) -> None:
    assert check_tokens.delay().get() == 0


def test_worker_without_the_meta_app_fails_clearly(services: Services) -> None:
    with pytest.raises(FacebookNotConfigured):
        assert services.facebook
    with pytest.raises(FacebookNotConfigured):
        assert services.facebook_box


def test_insights_enforce_the_monthly_limit_and_alerts_go_by_email(
    services: Services, facebook: FakeFacebook
) -> None:
    company_id, profile = _profile(services)
    sync_profile.delay(str(company_id), str(profile.id)).get()
    with services.uow(company_id) as uow:
        account = uow.facebook_accounts.list_for_profile(profile.id)[0]
        account.monthly_limit_micros = 1_000_000
        account.on_limit = FacebookOnLimit.PAUSE
        uow.commit()
    sync_insights.delay(str(company_id), str(account.id)).get()
    assert facebook.statuses == [("c1", "PAUSED")]
    with services.uow(company_id) as uow:
        campaign = uow.facebook_objects.get_by_external(company_id, "c1")
        assert campaign is not None and campaign.paused_by_limit_at is not None
    sync_insights.delay(str(company_id), str(account.id)).get()
    assert facebook.statuses == [("c1", "PAUSED")]
    assert email_alerts.delay().get() >= 1
    assert email_alerts.delay().get() == 0


def test_rules_run_without_rules(services: Services, facebook: FakeFacebook) -> None:
    _profile(services)
    assert schedule_rules.delay().get() == 0


def test_run_job_duplicates_once_and_tells_the_screen(
    services: Services, facebook: FakeFacebook, monkeypatch: pytest.MonkeyPatch
) -> None:
    published: list[tuple[str, dict[str, str]]] = []
    monkeypatch.setattr(
        "avant_worker.tasks.facebook.facebook_tasks.publish",
        lambda client, company, kind, data: published.append((kind, data)),
    )
    company_id, profile = _profile(services)
    sync_profile.delay(str(company_id), str(profile.id)).get()
    now = services.clock.now()
    with services.uow(company_id) as uow:
        account = uow.facebook_accounts.list_for_profile(profile.id)[0]
        job = FacebookJob(
            company_id=company_id,
            account_id=account.id,
            kind=FacebookJobKind.DUPLICATE,
            state=FacebookJobState.QUEUED,
            payload={"level": "campaign"},
            created_at=now,
            updated_at=now,
            created_by=profile.user_id,
            target_external_id="c1",
        )
        uow.facebook_jobs.add(job)
        uow.commit()
    calls_before = facebook.calls["ad_accounts"]
    assert run_job.delay(str(company_id), str(job.id)).get() == "done"
    assert facebook.calls["ad_accounts"] == calls_before + 1
    assert run_job.delay(str(company_id), str(job.id)).get() == "skipped"
    assert facebook.calls["copy"] == 1
    with services.uow(company_id) as uow:
        finished = uow.facebook_jobs.get(job.id)
        assert finished is not None and finished.created == {"copy": "c1-copia"}
    expected = ("facebook.job.updated", {"job_id": str(job.id)})
    assert published and all(event == expected for event in published)
