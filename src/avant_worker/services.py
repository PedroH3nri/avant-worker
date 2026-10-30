"""Os adaptadores que as tarefas entregam aos casos de uso. Um por processo.

O Celery cria os processos filhos com fork: cada filho monta o próprio pool de conexões
na primeira tarefa, nunca herda o do pai.
"""

import os
import uuid
from collections.abc import Iterable, Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Protocol

import redis
from avant_core.db.mapping import map_entities
from avant_core.db.uow import SqlAlchemyUnitOfWork
from avant_core.gam.client.models import Gam
from avant_core.mail import LogMailer, ResendMailer
from avant_core.metrics.models import GamMcmEarning, GamReportRow, PageViewCount
from avant_core.ports import Mailer
from avant_core.shared.clock import Clock, SystemClock
from sqlalchemy import Engine, create_engine

from avant_worker.adapters.exchange_rates import OpenExchangeRates
from avant_worker.adapters.gam_client import RestGamClient
from avant_worker.adapters.gam_reports import ReportKind, SoapReportClient
from avant_worker.adapters.page_views import MongoPageViews
from avant_worker.settings import Settings


class ReportSource(Protocol):
    """O que as tarefas de métricas pedem ao GAM: as linhas de um relatório."""

    def report(
        self, network_code: str, kind: ReportKind, start: date, end: date
    ) -> Iterable[GamReportRow]:
        """Linhas do relatório da network no período."""
        ...


class PageViewSource(Protocol):
    """O que a tarefa das visitas pede ao data: as contagens de uma network."""

    def counts(self, network_code: str, start: date, end: date) -> list[PageViewCount]:
        """Visitas por domínio, hora e país da network no período."""
        ...


class ExchangeRateSource(Protocol):
    """O que a tarefa das cotações pede: 1 USD em cada moeda, agora ou no fim de um dia."""

    def latest(self) -> dict[str, Decimal]:
        """Cotações de agora."""
        ...

    def historical(self, day: date) -> dict[str, Decimal]:
        """Cotações do fim do dia."""
        ...


class EarningsSource(Protocol):
    """O que a tarefa dos ganhos do MCM pede ao GAM: os ganhos do mês de cada filho."""

    def list_mcm_earnings(self, network_code: str, month: date) -> Iterable[GamMcmEarning]:
        """Ganhos do mês de cada filho do MCM da network."""
        ...


class GamNotConfigured(RuntimeError):
    """Tarefa da fila gam num worker sem a chave da conta de serviço."""


@dataclass
class Services:
    settings: Settings
    engine: Engine
    clock: Clock
    mailer: Mailer = field(default_factory=lambda: LogMailer(base_url="", show_links=False))
    redis: "redis.Redis | None" = None
    # Montado na primeira tarefa do GAM (ou entregue pronto nos testes).
    gam_override: Gam | None = None
    reports_override: "ReportSource | None" = None
    page_views_override: "PageViewSource | None" = None
    exchange_rates_override: "ExchangeRateSource | None" = None
    earnings_override: "EarningsSource | None" = None

    def __post_init__(self) -> None:
        # Entidades criadas por uma tarefa antes do primeiro Unit of Work já saem mapeadas.
        map_entities()
        self._gam: Gam | None = self.gam_override
        self._reports: ReportSource | None = self.reports_override
        self._page_views: PageViewSource | None = self.page_views_override
        self._exchange_rates: ExchangeRateSource | None = self.exchange_rates_override
        self._earnings: EarningsSource | None = self.earnings_override
        self._held: dict[str, redis.lock.Lock] = {}

    @classmethod
    def build(cls, settings: Settings) -> "Services":
        """Monta banco, Redis e email a partir das configurações."""
        engine = create_engine(
            settings.database_url, pool_size=settings.db_pool_size, pool_pre_ping=True
        )
        return cls(
            settings=settings,
            engine=engine,
            clock=SystemClock(),
            mailer=_mailer(settings),
            redis=redis.Redis.from_url(settings.redis_url) if settings.redis_url else None,
        )

    def uow(self, company_id: uuid.UUID) -> SqlAlchemyUnitOfWork:
        """Transação presa a uma Empresa (RLS)."""
        return SqlAlchemyUnitOfWork(self.engine, company_id=company_id)

    def trusted_uow(self) -> SqlAlchemyUnitOfWork:
        """Sem RLS: só para limpeza e para varrer todas as Empresas."""
        return SqlAlchemyUnitOfWork(self.engine, bypass_rls=True)

    @property
    def gam(self) -> Gam:
        """Monta o cliente do GAM na primeira vez que é usado; só a fila gam tem a chave."""
        if self._gam is None:
            settings = self.settings
            if not (settings.gam_service_account_file and settings.gam_groone_network_code):
                raise GamNotConfigured(
                    "defina GAM_SERVICE_ACCOUNT_FILE e GAM_GROONE_NETWORK_CODE neste worker"
                )
            self._gam = Gam(
                client=RestGamClient.from_key_file(settings.gam_service_account_file),
                groone_network_code=settings.gam_groone_network_code,
            )
        return self._gam

    @property
    def reports(self) -> "ReportSource":
        """Relatórios de métricas do GAM (SOAP, só leitura); só a fila gam tem a chave."""
        if self._reports is None:
            key_file = self.settings.gam_service_account_file
            if not key_file:
                raise GamNotConfigured("defina GAM_SERVICE_ACCOUNT_FILE neste worker")
            self._reports = SoapReportClient(key_file, version=self.settings.gam_soap_version)
        return self._reports

    @property
    def earnings(self) -> "EarningsSource":
        """Ganhos do MCM pela API REST do GAM (só leitura); só a fila gam tem a chave."""
        if self._earnings is None:
            key_file = self.settings.gam_service_account_file
            if not key_file:
                raise GamNotConfigured("defina GAM_SERVICE_ACCOUNT_FILE neste worker")
            self._earnings = RestGamClient.from_key_file(key_file)
        return self._earnings

    @property
    def page_views(self) -> "PageViewSource | None":
        """Visitas do data (Mongo, só leitura); ``None`` quando o worker não tem a URL."""
        if self._page_views is None and self.settings.page_views_mongo_url:
            self._page_views = MongoPageViews(
                self.settings.page_views_mongo_url, self.settings.page_views_mongo_database
            )
        return self._page_views

    @property
    def exchange_rates(self) -> "ExchangeRateSource | None":
        """Cotações do Open Exchange Rates; ``None`` quando o worker não tem a chave."""
        if self._exchange_rates is None and self.settings.openexchangerates_app_id:
            self._exchange_rates = OpenExchangeRates(self.settings.openexchangerates_app_id)
        return self._exchange_rates

    @contextmanager
    def lock(self, key: str, *, timeout: int) -> Iterator[bool]:
        """Trava no Redis (``True`` se conseguiu). Sem Redis, não trava: só no local."""
        if self.redis is None:
            yield True
            return
        lock = self.redis.lock(f"avant:lock:{key}", timeout=timeout, blocking=False)
        if not lock.acquire():
            yield False
            return
        self._held[key] = lock
        try:
            yield True
        finally:
            self._held.pop(key, None)
            # Passou do tempo da trava: outra execução já pode ter pegado; não é erro.
            with suppress(redis.exceptions.LockError):
                lock.release()

    def renew_lock(self, key: str, *, timeout: int) -> None:
        """Dá mais ``timeout`` segundos à trava que esta execução segura, para um trabalho longo
        não perder a trava no meio."""
        lock = self._held.get(key)
        if lock is None:
            return
        with suppress(redis.exceptions.LockError):
            lock.extend(timeout, replace_ttl=True)


def _mailer(settings: Settings) -> Mailer:
    """Usa o Resend quando há chave; senão só registra os emails no log."""
    if settings.resend_api_key:
        return ResendMailer(
            api_key=settings.resend_api_key,
            sender=settings.mail_from,
            base_url=settings.app_base_url,
        )
    return LogMailer(base_url=settings.app_base_url, show_links=settings.avant_env == "local")


_current: tuple[int, Services] | None = None


def get_services() -> Services:
    """Devolve os serviços do processo, montando de novo depois de um fork."""
    global _current
    if _current is None or _current[0] != os.getpid():
        _current = (os.getpid(), Services.build(Settings()))
    return _current[1]


def use_services(services: Services | None) -> None:
    """Para os testes: troca os serviços do processo."""
    global _current
    _current = (os.getpid(), services) if services else None
