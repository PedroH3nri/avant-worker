"""Tarefas da segurança do site."""

from avant_worker.tasks.site_security.site_integrity_tasks import aggregate_site_integrity

__all__ = ["aggregate_site_integrity"]
