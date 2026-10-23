"""Os adaptadores que as tarefas entregam aos casos de uso. Um por processo.

O Celery cria os processos filhos com fork: cada filho monta o próprio pool de conexões
na primeira tarefa, nunca herda o do pai.
"""

import os
import uuid
from dataclasses import dataclass

from avant_core.db.mapping import map_entities
from avant_core.db.uow import SqlAlchemyUnitOfWork
from avant_core.shared.clock import Clock, SystemClock
from sqlalchemy import Engine, create_engine

from avant_worker.settings import Settings


@dataclass
class Services:
    settings: Settings
    engine: Engine
    clock: Clock

    def __post_init__(self) -> None:
        # Entidades criadas por uma tarefa antes do primeiro Unit of Work já saem mapeadas.
        map_entities()

    @classmethod
    def build(cls, settings: Settings) -> "Services":
        engine = create_engine(
            settings.database_url, pool_size=settings.db_pool_size, pool_pre_ping=True
        )
        return cls(settings=settings, engine=engine, clock=SystemClock())

    def uow(self, company_id: uuid.UUID) -> SqlAlchemyUnitOfWork:
        """Transação presa a uma Empresa (RLS)."""
        return SqlAlchemyUnitOfWork(self.engine, company_id=company_id)

    def trusted_uow(self) -> SqlAlchemyUnitOfWork:
        """Sem RLS: só para limpeza e para varrer todas as Empresas."""
        return SqlAlchemyUnitOfWork(self.engine, bypass_rls=True)


_current: tuple[int, Services] | None = None


def get_services() -> Services:
    global _current
    if _current is None or _current[0] != os.getpid():
        _current = (os.getpid(), Services.build(Settings()))
    return _current[1]


def use_services(services: Services | None) -> None:
    """Para os testes: troca os serviços do processo."""
    global _current
    _current = (os.getpid(), services) if services else None
