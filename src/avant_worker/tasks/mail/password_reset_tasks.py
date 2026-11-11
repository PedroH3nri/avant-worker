"""Tarefa do esqueci a senha (fila ``mail``).

A API só enfileira o e-mail digitado, sem ler o banco, para a resposta ter o mesmo tempo
exista ou não a conta. O token nasce aqui, dentro do caso de uso, e nunca passa pela fila nem
pelo log (o e-mail também não é registrado).

``trusted_uow``: quem pede a nova senha ainda não tem sessão nem Empresa ativa.

Em falha, tenta de novo (30 s, 1, 2 e 4 minutos). Cada tentativa que falha depois de gravar
deixa um pedido a mais; o limite de pedidos por hora do caso de uso (3) encerra as tentativas
em silêncio, e só uma tentativa chega a enviar o e-mail. Com ``acks_late`` o pior caso é um
e-mail repetido com um link válido, nunca um e-mail perdido.
"""

from avant_core.identity.services import request_password_reset as request_password_reset_use_case

from avant_worker.app import app
from avant_worker.services import get_services

RETRY_BACKOFF_SECONDS = 30
RETRY_BACKOFF_MAX_SECONDS = 4 * 60
MAX_RETRIES = 4


@app.task(
    name="avant.mail.request_password_reset",
    autoretry_for=(Exception,),
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
