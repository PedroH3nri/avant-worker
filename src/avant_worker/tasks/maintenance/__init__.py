"""Tarefas de limpeza."""

from avant_worker.tasks.maintenance.purge_tasks import purge_expired

__all__ = ["purge_expired"]
