"""Tarefas da integração com o HubSpot."""

from avant_worker.tasks.hubspot.hubspot_tasks import sync_hubspot

__all__ = ["sync_hubspot"]
