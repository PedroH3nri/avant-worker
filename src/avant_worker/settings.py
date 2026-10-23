"""Configuração por variáveis de ambiente. Os valores reais ficam só nas VMs."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class BrokerSettings(BaseSettings):
    """O que o agendador precisa: ele só publica tarefas, não fala com o banco."""

    model_config = SettingsConfigDict(extra="ignore")

    avant_env: Literal["local", "test", "staging", "production"] = "local"
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    # Resultados das tarefas. Sem Redis, as tarefas rodam sem guardar resultado.
    redis_url: str | None = None


class Settings(BrokerSettings):
    # Papel avant_app: sem BYPASSRLS e sem ser dono das tabelas.
    database_url: str
    db_pool_size: int = 5
