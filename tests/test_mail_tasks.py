import smtplib
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
from avant_core.company.enums import InvitationKind
from avant_core.identity.models import User
from avant_core.identity.models.password_reset import PASSWORD_RESETS_PER_HOUR
from avant_core.mail import ResendMailer, SmtpMailer
from avant_core.ports import MailNotSent, Notice
from celery.app.task import Task
from celery.contrib.testing.mocks import TaskMessage
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import TimeoutError as PoolTimeout

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.mail import password_reset_tasks, request_password_reset
from avant_worker.tasks.mail.password_reset_tasks import (
    MAX_RETRIES,
    MaskedRequest,
    TemporaryDatabaseError,
)

EMAIL = "ana@acai.com.br"


@dataclass
class RecordingMailer:
    """Guarda os e-mails de nova senha que sairiam; pode falhar nas primeiras tentativas."""

    resets: list[tuple[str, str, str]] = field(default_factory=list)
    failures_left: int = 0

    def send_invitation(
        self, *, to: str, token: str, kind: InvitationKind, company_name: str | None, locale: str
    ) -> None:
        """Não usado aqui."""

    def send_password_reset(self, *, to: str, token: str, locale: str) -> None:
        """Guarda o envio, ou falha enquanto restarem falhas programadas."""
        if self.failures_left:
            self.failures_left -= 1
            raise MailNotSent("provedor de e-mail fora do ar")
        self.resets.append((to, token, locale))

    def send_notice(
        self, *, to: str, notice: Notice, locale: str, params: dict[str, str] | None = None
    ) -> None:
        """Não usado aqui."""

    def send_metric_alert(self, *, to: str, locale: str, alert: object) -> None:
        """Não usado aqui."""

    def send_scheduled_report(self, *, to: str, locale: str, report: object) -> None:
        """Não usado aqui."""


def add_user(services: Services, email: str) -> None:
    """Grava um usuário ativo com o e-mail."""
    with services.trusted_uow() as uow:
        uow.users.add(User(email=email, name="Ana"))
        uow.commit()


def count_resets(services: Services) -> int:
    """Quantos pedidos de nova senha estão gravados."""
    with services.trusted_uow() as uow:
        return int(uow.session.execute(text("SELECT count(*) FROM password_resets")).scalar_one())


def test_password_reset_task_is_registered_on_the_mail_queue() -> None:
    app.loader.import_default_modules()
    assert _route("avant.mail.request_password_reset") == {"queue": "mail"}
    assert "avant.mail.request_password_reset" in app.tasks


def test_password_reset_task_has_a_bounded_retry() -> None:
    assert request_password_reset.max_retries == MAX_RETRIES


def test_task_sends_the_reset_email_with_a_token_generated_here(services: Services) -> None:
    add_user(services, "ana@acai.com.br")
    mailer = RecordingMailer()
    services.mailer = mailer
    request_password_reset.delay("ana@acai.com.br")
    assert [(to, locale) for to, _, locale in mailer.resets] == [("ana@acai.com.br", "pt")]
    assert mailer.resets[0][1]
    assert count_resets(services) == 1


def test_task_ends_silently_when_the_account_does_not_exist(services: Services) -> None:
    mailer = RecordingMailer()
    services.mailer = mailer
    request_password_reset.delay("ninguem@acai.com.br")
    assert mailer.resets == []
    assert count_resets(services) == 0


def test_the_real_resend_mailer_failing_makes_the_task_try_again(services: Services) -> None:
    add_user(services, EMAIL)
    statuses = [503, 503, 200]
    sent: list[int] = []

    def resend(request: httpx.Request) -> httpx.Response:
        """O Resend responde 503 duas vezes (a primeira tentativa inteira) e depois aceita."""
        status = statuses.pop(0)
        sent.append(status)
        return httpx.Response(status, json={"id": "re_1"} if status == 200 else {})

    services.mailer = ResendMailer(
        api_key="re_teste",
        sender="Avant <nao-responda@avant.groone.com>",
        base_url="https://avant.groone.com",
        client=httpx.Client(transport=httpx.MockTransport(resend)),
    )
    request_password_reset.delay(EMAIL)
    assert sent == [503, 503, 200]
    assert count_resets(services) == 2


def test_the_smtp_mailer_failing_for_now_makes_the_task_try_again(
    services: Services, monkeypatch: pytest.MonkeyPatch
) -> None:
    add_user(services, EMAIL)
    replies: list[int] = [421, 421, 250]
    delivered: list[int] = []

    class FakeSmtp:
        """Servidor SMTP que responde 421 (ocupado) duas vezes e depois aceita."""

        def __init__(self, host: str, port: int, timeout: float) -> None:
            self.host = host

        def send_message(self, email: Any, to_addrs: list[str]) -> None:
            """Aceita ou recusa por agora, na ordem programada."""
            code = replies.pop(0)
            delivered.append(code)
            if code != 250:
                raise smtplib.SMTPResponseException(code, b"ocupado, tente depois")

        def quit(self) -> None:
            """Encerra a conversa."""

        def close(self) -> None:
            """Fecha o socket."""

    monkeypatch.setattr(smtplib, "SMTP", FakeSmtp)
    services.mailer = SmtpMailer(
        url="smtp://mailpit:1025",
        sender="Avant <nao-responda@avant.groone.com>",
        base_url="https://avant.groone.com",
    )
    request_password_reset.delay(EMAIL)
    assert delivered == [421, 421, 250]
    assert count_resets(services) == 2


def test_an_error_that_is_not_temporary_is_not_retried(services: Services) -> None:
    add_user(services, EMAIL)

    @dataclass
    class BrokenMailer(RecordingMailer):
        """Falha com um erro de programação, que não se resolve tentando de novo."""

        def send_password_reset(self, *, to: str, token: str, locale: str) -> None:
            """Sempre quebra."""
            raise ValueError("bug")

    services.mailer = BrokenMailer()
    request_password_reset.delay(EMAIL)
    assert count_resets(services) == 1


def test_the_email_never_reaches_the_celery_log_or_events() -> None:
    message = TaskMessage(
        "avant.mail.request_password_reset",
        args=(EMAIL,),
        argsrepr=repr((EMAIL,)),
        kwargsrepr=repr({"email": EMAIL}),
    )
    request = MaskedRequest(message, app=app, task=request_password_reset)
    assert EMAIL not in request.argsrepr + request.kwargsrepr
    assert EMAIL not in str(request.info(safe=True))
    assert EMAIL not in str(request.request_dict.get("argsrepr"))
    assert EMAIL not in str(request.request_dict.get("kwargsrepr"))


@pytest.mark.parametrize(
    "database_error",
    [
        OperationalError(
            "SELECT * FROM users WHERE email = %(email)s", {"email": EMAIL}, Exception("caiu")
        ),
        PoolTimeout(f"pool cheio ao buscar {EMAIL}"),
    ],
)
def test_a_database_error_retries_without_the_email(
    monkeypatch: pytest.MonkeyPatch, database_error: Exception
) -> None:
    def failing_use_case(*_: Any, **__: Any) -> None:
        """O banco falha com o e-mail nos parâmetros."""
        raise database_error

    monkeypatch.setattr(password_reset_tasks, "request_password_reset_use_case", failing_use_case)
    monkeypatch.setattr(
        password_reset_tasks,
        "get_services",
        lambda: SimpleNamespace(trusted_uow=lambda: None, clock=None, mailer=None),
    )
    with pytest.raises(TemporaryDatabaseError) as raised:
        request_password_reset._orig_run(EMAIL)  # type: ignore[attr-defined]
    error = raised.value
    assert EMAIL not in str(error) + repr(error) + repr(error.args)
    assert error.__cause__ is None and error.__context__ is None
    assert TemporaryDatabaseError in request_password_reset.autoretry_for  # type: ignore[attr-defined]


def test_a_retry_publishes_the_email_masked(monkeypatch: pytest.MonkeyPatch) -> None:
    published: list[dict[str, Any]] = []

    def capture(
        self: "Task[Any, Any]", args: Any = None, kwargs: Any = None, **options: Any
    ) -> None:
        """Guarda as opções da publicação em vez de publicar."""
        published.append(options)

    monkeypatch.setattr(Task, "apply_async", capture)
    request_password_reset.apply_async(args=(EMAIL,))
    assert EMAIL not in published[0]["argsrepr"] + published[0]["kwargsrepr"]


def test_persistent_failure_stops_at_the_hourly_limit_without_sending(
    services: Services,
) -> None:
    add_user(services, "ana@acai.com.br")
    mailer = RecordingMailer(failures_left=100)
    services.mailer = mailer
    request_password_reset.delay("ana@acai.com.br")
    assert mailer.resets == []
    assert count_resets(services) == PASSWORD_RESETS_PER_HOUR
