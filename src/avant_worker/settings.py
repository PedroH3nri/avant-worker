"""Configuração por variáveis de ambiente. Os valores reais ficam só nas VMs."""

from avant_core.db.engine import EngineSettings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

APPLICATION_NAME = "avant-worker"
REDIS_SCHEME = r"^rediss?://"
NOT_BLANK = r"\S"


class BrokerSettings(BaseSettings):
    """O que o agendador precisa: ele só publica tarefas, não fala com o banco."""

    model_config = SettingsConfigDict(extra="ignore")

    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    # Resultados das tarefas. O agendador só publica; o worker exige o Redis (``Settings``).
    redis_url: str | None = None


class Settings(BrokerSettings):
    """O que o worker precisa. Redis e Resend são obrigatórios em todo ambiente: sem eles, o
    worker não sobe (no desenvolvimento, uma chave do Resend com remetente de sandbox)."""

    # Papel avant_app: sem BYPASSRLS e sem ser dono das tabelas.
    database_url: str = Field(min_length=1)
    # Pool e prazos de cada processo filho, iguais em todo ambiente (tetos no avant-core).
    db_pool_size: int = 5
    db_max_overflow: int = 0
    db_pool_timeout_seconds: float = 30
    db_pool_recycle_seconds: int = 1800
    db_statement_timeout_ms: int = 300_000
    db_idle_in_transaction_timeout_ms: int = 60_000
    db_lock_timeout_ms: int = 30_000
    redis_url: str = Field(min_length=1, pattern=REDIS_SCHEME)

    # E-mails: sempre pelo Resend; nenhum link com token vai para o log.
    app_base_url: str = "http://localhost:8080"
    resend_api_key: str = Field(min_length=1, pattern=NOT_BLANK)
    mail_from: str = "Avant <nao-responda@avant.groone.com>"

    # Google Ad Manager: só os workers da fila gam têm a chave da conta de serviço.
    gam_service_account_file: str | None = None
    gam_groone_network_code: str | None = None
    # Versão da API SOAP dos relatórios (ex.: v202608); vazio usa a mais nova do googleads.
    gam_soap_version: str | None = None

    # Visitas: o Mongo do iGroone/data (só leitura). Sem URL, a tarefa das visitas não roda.
    page_views_mongo_url: str | None = None
    page_views_mongo_database: str = "admanager"

    # País das visitas da tag pelo IP: a base GeoLite2 Country (.mmdb). Sem ela, o país fica
    # "unknown" e as visitas são gravadas do mesmo jeito.
    geolite2_country_file: str | None = None

    # Cotações do dia (Open Exchange Rates). Sem chave, a tarefa das cotações não roda.
    openexchangerates_app_id: str | None = None

    def engine_settings(self) -> EngineSettings:
        """O pool e os prazos do Postgres deste worker, com o nome ``avant-worker``."""
        return EngineSettings(
            application_name=APPLICATION_NAME,
            pool_size=self.db_pool_size,
            max_overflow=self.db_max_overflow,
            pool_timeout_seconds=self.db_pool_timeout_seconds,
            pool_recycle_seconds=self.db_pool_recycle_seconds,
            statement_timeout_ms=self.db_statement_timeout_ms,
            idle_in_transaction_timeout_ms=self.db_idle_in_transaction_timeout_ms,
            lock_timeout_ms=self.db_lock_timeout_ms,
        )
