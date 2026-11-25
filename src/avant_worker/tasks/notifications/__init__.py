"""Tarefas das notificações do sino."""

from avant_worker.tasks.notifications.notification_tasks import purge_old_notifications

__all__ = ["purge_old_notifications"]
