"""Tarefas da fila ``mail`` (e-mails que a API pede sem esperar o envio)."""

from avant_worker.tasks.mail.password_reset_tasks import request_password_reset

__all__ = ["request_password_reset"]
