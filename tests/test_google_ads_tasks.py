"""Google Ads: o agendador manda uma tarefa por login e por conta, que grava contas, estrutura,
números e histórico na Empresa; erro temporário tenta de novo e worker sem o cliente falha
claro."""

import uuid
from datetime import date, datetime
from typing import Any

import pytest
from avant_core.google_ads.enums import (
    GoogleAdsAccountStatus,
    GoogleAdsLevel,
    GoogleAdsOnLimit,
)
from avant_core.google_ads.errors import GoogleAdsUnavailable
from avant_core.google_ads.models import (
    GoogleAdsAccountData,
    GoogleAdsCampaignRow,
    GoogleAdsChangeData,
    GoogleAdsKeywordData,
    GoogleAdsKeywordRow,
    GoogleAdsLogin,
    GoogleAdsMetricRow,
    GoogleAdsObjectData,
    GoogleAdsPlacementRow,
    GoogleAdsRule,
    GoogleAdsSearchTermRow,
    GoogleAdsToken,
)
from avant_core.identity.security.crypto import FernetSecretBox
from celery.exceptions import Retry
from cryptography.fernet import Fernet
from sqlalchemy import text

from avant_worker.app import _route, app
from avant_worker.services import GoogleAdsNotConfigured, Services
from avant_worker.tasks.google_ads import (
    schedule_changes,
    schedule_metrics,
    schedule_rules,
    schedule_structure,
    sync_changes,
    sync_login,
)
from tests.test_gam_tasks import company

CUSTOMER = "1234567890"


class FakeGoogleAds:
    """A API do Google Ads com uma conta numa MCC, uma campanha com grupo, anúncio e palavra."""

    def __init__(self) -> None:
        self.unavailable = False
        self.calls: list[str] = []

    def exchange_code(self, code: str, redirect_uri: str) -> GoogleAdsToken:
        """Não usado pelo worker."""
        raise NotImplementedError

    def accounts(self, token: str) -> list[GoogleAdsAccountData]:
        """A conta de teste, ou o erro temporário."""
        self.calls.append("accounts")
        if self.unavailable:
            raise GoogleAdsUnavailable("cota esgotada")
        return [
            GoogleAdsAccountData(
                CUSTOMER,
                "Blog",
                "5550001111",
                "MCC",
                "BRL",
                "America/Sao_Paulo",
                GoogleAdsAccountStatus.ENABLED,
            )
        ]

    def objects(self, token: str, login: str, customer_id: str) -> list[GoogleAdsObjectData]:
        """Campanha, grupo e anúncio."""
        return [
            GoogleAdsObjectData(GoogleAdsLevel.CAMPAIGN, "111", "Bolo", None, "111", "ENABLED"),
            GoogleAdsObjectData(GoogleAdsLevel.AD_GROUP, "222", "Cenoura", "111", "111", "ENABLED"),
            GoogleAdsObjectData(GoogleAdsLevel.AD, "333", "Anúncio", "222", "111", "ENABLED"),
        ]

    def keywords(self, token: str, login: str, customer_id: str) -> list[GoogleAdsKeywordData]:
        """Uma palavra-chave no grupo."""
        return [GoogleAdsKeywordData("222", "111", "44", "bolo", "PHRASE", "ENABLED")]

    def campaign_metrics(
        self, token: str, login: str, customer_id: str, since: date, until: date
    ) -> list[GoogleAdsCampaignRow]:
        """Uma linha por campanha no último dia."""
        return [GoogleAdsCampaignRow("111", until, 5_000_000, 1000, 30, 2)]

    def ad_metrics(
        self, token: str, login: str, customer_id: str, since: date, until: date
    ) -> list[GoogleAdsMetricRow]:
        """Uma linha por anúncio no último dia."""
        return [GoogleAdsMetricRow("333", "222", "111", until, 5_000_000, 1000, 30, 2)]

    def keyword_metrics(
        self, token: str, login: str, customer_id: str, since: date, until: date
    ) -> list[GoogleAdsKeywordRow]:
        """Uma linha por palavra-chave no último dia."""
        return [GoogleAdsKeywordRow("222", "44", "111", until, 4_000_000, 800, 25, 2)]

    def search_terms(
        self, token: str, login: str, customer_id: str, since: date, until: date
    ) -> list[GoogleAdsSearchTermRow]:
        """Um termo de pesquisa, só na sincronia com termos."""
        self.calls.append("search_terms")
        return [GoogleAdsSearchTermRow("111", "222", "44", "bolo", until, 3_000_000, 500, 20, 1)]

    def placements(
        self, token: str, login: str, customer_id: str, since: date, until: date
    ) -> list[GoogleAdsPlacementRow]:
        """Sem posicionamentos."""
        return []

    def changes(
        self, token: str, login: str, customer_id: str, since: datetime, time_zone: str
    ) -> list[GoogleAdsChangeData]:
        """Sem mudanças."""
        self.calls.append("changes")
        return []

    def set_url_suffix(self, token: str, login: str, customer_id: str, suffix: str) -> None:
        """Não usado pelo worker."""

    def set_status(
        self,
        token: str,
        login: str,
        customer_id: str,
        level: GoogleAdsLevel,
        resource_id: str,
        status: str,
    ) -> None:
        """Guarda a mudança de situação."""
        self.calls.append(f"status:{resource_id}:{status}")

    def set_campaign_budget(
        self, token: str, login: str, customer_id: str, campaign_id: str, amount_micros: int
    ) -> None:
        """Guarda o orçamento novo."""
        self.calls.append(f"budget:{campaign_id}:{amount_micros}")

    def set_keyword(
        self,
        token: str,
        login: str,
        customer_id: str,
        ad_group_id: str,
        criterion_id: str,
        *,
        status: str | None = None,
        cpc_bid_micros: int | None = None,
    ) -> None:
        """Guarda a mudança da palavra-chave."""
        self.calls.append(f"keyword:{criterion_id}:{status}:{cpc_bid_micros}")

    def negate_term(
        self, token: str, login: str, customer_id: str, campaign_id: str, text: str
    ) -> str:
        """Não usado pelo worker."""
        raise NotImplementedError

    def exclude_placement(
        self,
        token: str,
        login: str,
        customer_id: str,
        campaign_id: str,
        placement: str,
        placement_type: str,
    ) -> str:
        """Não usado pelo worker."""
        raise NotImplementedError

    def revoke(self, token: str) -> None:
        """Não usado pelo worker."""


@pytest.fixture
def google_ads(services: Services) -> FakeGoogleAds:
    """Os serviços com a API do Google Ads falsa e uma chave de tokens nova."""
    fake = FakeGoogleAds()
    services._google_ads = fake
    services._google_ads_box = FernetSecretBox(Fernet.generate_key().decode())
    return fake


def _login(services: Services) -> tuple[uuid.UUID, GoogleAdsLogin]:
    """Uma Empresa com um login do Google conectado."""
    owner = company(services, email=f"dono-{uuid.uuid4().hex[:6]}@blog.com")
    login = GoogleAdsLogin(
        company_id=owner.id,
        user_id=owner.owner_user_id,
        google_user_id="google-1",
        email="dono@gmail.com",
        token_ciphertext=services.google_ads_box.encrypt("refresh-1"),
        connected_at=services.clock.now(),
    )
    with services.uow(owner.id) as uow:
        uow.google_ads_logins.add(login)
        uow.commit()
    return owner.id, login


def _count(services: Services, table: str) -> int:
    """Quantas linhas a tabela tem, sem RLS."""
    with services.trusted_uow() as uow:
        return int(uow.session.execute(text(f"SELECT count(*) FROM {table}")).scalar_one())


def test_tasks_go_to_the_google_ads_queue_and_retry_on_unavailable() -> None:
    for name in (
        "avant.google_ads.schedule_structure",
        "avant.google_ads.sync_login",
        "avant.google_ads.schedule_metrics",
        "avant.google_ads.sync_metrics",
        "avant.google_ads.schedule_changes",
        "avant.google_ads.sync_changes",
        "avant.google_ads.schedule_rules",
        "avant.google_ads.run_rules",
    ):
        assert name in app.tasks
        assert _route(name) == {"queue": "google_ads"}
    typed: Any = sync_login
    assert typed.autoretry_for == (GoogleAdsUnavailable,) and typed.max_retries == 4


def test_beat_runs_structure_hourly_and_metrics_every_thirty_minutes() -> None:
    schedule = app.conf.beat_schedule
    assert schedule["google-ads-structure"]["schedule"].minute == {35}
    assert schedule["google-ads-metrics-today"]["schedule"].minute == {5, 35}
    assert schedule["google-ads-metrics-late"]["kwargs"] == {"days": 3, "with_terms": True}
    assert schedule["google-ads-changes"]["task"] == "avant.google_ads.schedule_changes"
    yesterday = schedule["google-ads-metrics-yesterday"]
    assert (yesterday["schedule"].hour, yesterday["schedule"].minute) == ({8}, {45})
    assert yesterday["kwargs"] == {"days": 2}
    rules = schedule["google-ads-rules"]["schedule"]
    assert (rules.hour, rules.minute) == ({9}, {20})


def test_structure_metrics_and_changes_fill_the_company(
    services: Services, google_ads: FakeGoogleAds
) -> None:
    company_id, login = _login(services)
    assert schedule_structure.delay().get() == 1
    assert _count(services, "google_ads_accounts") == 1
    assert _count(services, "google_ads_objects") == 3
    assert _count(services, "google_ads_keywords") == 1
    assert schedule_metrics.delay().get() == 1
    assert _count(services, "metrics.google_ads_campaign_daily") == 1
    assert _count(services, "metrics.google_ads_daily") == 1
    assert "search_terms" not in google_ads.calls
    assert schedule_metrics.delay(3, True).get() == 1
    assert _count(services, "metrics.google_ads_search_term_daily") == 1
    assert schedule_changes.delay().get() == 1
    with services.uow(company_id) as uow:
        account = uow.google_ads_accounts.list_for_login(login.id)[0]
    assert sync_changes.delay(str(company_id), str(account.id)).get() == 0
    second = sync_login.delay(str(company_id), str(login.id)).get()
    assert second["error"] is None and _count(services, "google_ads_objects") == 3


def test_unavailable_is_retried(services: Services, google_ads: FakeGoogleAds) -> None:
    company_id, login = _login(services)
    google_ads.unavailable = True
    with pytest.raises(Retry):
        sync_login.apply(args=(str(company_id), str(login.id)), throw=True)


def test_worker_without_the_google_client_fails_clearly(services: Services) -> None:
    with pytest.raises(GoogleAdsNotConfigured):
        assert services.google_ads
    with pytest.raises(GoogleAdsNotConfigured):
        assert services.google_ads_box


def test_metrics_enforce_the_monthly_limit_and_rules_skip_accounts_without_site(
    services: Services, google_ads: FakeGoogleAds
) -> None:
    company_id, login = _login(services)
    schedule_structure.delay().get()
    with services.uow(company_id) as uow:
        account = uow.google_ads_accounts.list_for_login(login.id)[0]
        account.monthly_limit_micros = 1_000_000
        account.on_limit = GoogleAdsOnLimit.PAUSE
        uow.google_ads_rules.add(
            GoogleAdsRule(
                company_id=company_id,
                account_id=account.id,
                object_external_id="333",
                level=GoogleAdsLevel.AD,
                updated_at=services.clock.now(),
                pause=True,
                days=1,
            )
        )
        uow.commit()
    schedule_metrics.delay().get()
    assert "status:111:PAUSED" in google_ads.calls
    assert _count(services, "google_ads_alerts") == 1
    assert schedule_rules.delay().get() == 1
    assert _count(services, "google_ads_rule_decisions") == 0
