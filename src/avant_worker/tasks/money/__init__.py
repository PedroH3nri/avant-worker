"""Tarefas de moeda: cotações."""

from avant_worker.tasks.money.exchange_rate_tasks import closed_days_to_fetch, sync_exchange_rates

__all__ = ["closed_days_to_fetch", "sync_exchange_rates"]
