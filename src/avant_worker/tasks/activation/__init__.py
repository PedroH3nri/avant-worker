"""Tarefas do funil de ativação."""

from avant_worker.tasks.activation.activation_tasks import record_activation

__all__ = ["record_activation"]
