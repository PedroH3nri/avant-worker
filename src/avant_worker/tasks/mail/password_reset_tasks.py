"""Tarefa do esqueci a senha (fila ``mail``).

A API só enfileira o e-mail digitado, sem ler o banco, para a resposta ter o mesmo tempo
exista ou não a conta. O token nasce aqui, dentro do caso de uso, e nunca passa pela fila nem
pelo log. O e-mail também fica fora do log e dos eventos do Celery (que o celery-exporter lê):
o ``MaskedRequest`` mascara os argumentos que o worker registra e publica, e uma nova tentativa
sai com os argumentos mascarados no cabeçalho da mensagem.

``trusted_uow``: quem pede a nova senha ainda não tem sessão nem Empresa ativa.

Só repete em erro temporário: o e-mail que não saiu (``MailNotSent``, depois das duas tentativas
do ``ResendMailer``) e a falha de conexão ou prazo do banco. Espera 30 s, 1, 2 e 4 minutos.
Cada tentativa grava um link novo antes de enviar, então no pior caso a pessoa tem até 3 links
válidos na mesma hora; o limite de 3 pedidos por hora do caso de uso encerra as tentativas em
silêncio. Com ``acks_late``, o pior caso é um e-mail repetido, nunca um e-mail perdido.
"""

from typing import Any

from avant_core.identity.services import request_password_reset as request_password_reset_use_case
from avant_core.ports import MailNotSent
from celery import Task
from celery.result import AsyncResult
from celery.worker.request import Request
from sqlalchemy.exc import OperationalError

from avant_worker.app import app
from avant_worker.services import get_services

RETRY_BACKOFF_SECONDS = 30
RETRY_BACKOFF_MAX_SECONDS = 4 * 60
MAX_RETRIES = 4
TEMPORARY_ERRORS = (MailNotSent, OperationalError)
MASKED_ARGS = "('***',)"
MASKED_KWARGS = "{}"


class MaskedRequest(Request):
    """O pedido da tarefa com os argumentos mascarados no log e nos eventos do Celery."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._argsrepr = MASKED_ARGS
        self._kwargsrepr = MASKED_KWARGS


class MaskedTask(Task):  # type: ignore[type-arg]
    """Tarefa que publica (inclusive ao tentar de novo) com os argumentos mascarados."""

    Request = "avant_worker.tasks.mail.password_reset_tasks:MaskedRequest"

    def apply_async(  # type: ignore[override]
        self, args: Any = None, kwargs: Any = None, **options: Any
    ) -> "AsyncResult[Any]":
        """Publica com ``argsrepr`` e ``kwargsrepr`` mascarados."""
        options.update(argsrepr=MASKED_ARGS, kwargsrepr=MASKED_KWARGS)
        return super().apply_async(args, kwargs, **options)


@app.task(
    base=MaskedTask,
    name="avant.mail.request_password_reset",
    autoretry_for=TEMPORARY_ERRORS,
    retry_backoff=RETRY_BACKOFF_SECONDS,
    retry_backoff_max=RETRY_BACKOFF_MAX_SECONDS,
    retry_jitter=False,
    max_retries=MAX_RETRIES,
)
def request_password_reset(email: str) -> None:
    """trusted_uow: gera o token e manda o e-mail de nova senha, se a conta existir."""
    services = get_services()
    request_password_reset_use_case(
        services.trusted_uow(), email=email, clock=services.clock, mailer=services.mailer
    )
