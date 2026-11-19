"""Tarefas da integração com o Google Ads: contas, estrutura, números e histórico."""

from avant_worker.tasks.google_ads.google_ads_tasks import (
    LATE_DAYS,
    schedule_changes,
    schedule_metrics,
    schedule_structure,
    sync_changes,
    sync_login,
    sync_metrics,
)

__all__ = [
    "LATE_DAYS",
    "schedule_changes",
    "schedule_metrics",
    "schedule_structure",
    "sync_changes",
    "sync_login",
    "sync_metrics",
]
