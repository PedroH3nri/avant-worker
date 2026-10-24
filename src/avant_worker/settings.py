"""Configuração por variáveis de ambiente. Os valores reais ficam só nas VMs."""

from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrokerSettings(BaseSettings):
    """O que o agendador precisa: ele só publica tarefas, não fala com o banco."""

    model_config = SettingsConfigDict(extra="ignore")

    avant_env: Literal["local", "test", "staging", "production"] = "local"
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    # Resultados das tarefas e trava por network. Sem Redis, só no local e nos testes.
    redis_url: str | None = None


class Settings(BrokerSettings):
    # Papel avant_app: sem BYPASSRLS e sem ser dono das tabelas.
    database_url: str
    db_pool_size: int = 5

    # E-mails (avisos de network com erro ou desconectada). Sem chave, só no log.
    app_base_url: str = "http://localhost:8080"
    resend_api_key: str | None = None
    mail_from: str = "Avant <nao-responda@avant.groone.com>"

    # Google Ad Manager: só os workers da fila gam têm a chave da conta de serviço.
    gam_service_account_file: str | None = None
    gam_groone_network_code: str | None = None
    # Versão da API SOAP dos relatórios (ex.: v202608); vazio usa a mais nova do googleads.
    gam_soap_version: str | None = None

    @model_validator(mode="after")
    def _deployed_envs(self) -> "Settings":
        """Exige as variáveis obrigatórias em staging e produção."""
        if self.avant_env in ("staging", "production"):
            missing = [
                name
                for name, value in (
                    ("REDIS_URL", self.redis_url),
                    ("RESEND_API_KEY", self.resend_api_key),
                )
                if not value
            ]
            if missing:
                raise ValueError(f"faltam variáveis em {self.avant_env}: {', '.join(missing)}")
        return self
