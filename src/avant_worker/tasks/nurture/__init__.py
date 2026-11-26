"""Tarefas das réguas de nutrição."""

from avant_worker.tasks.nurture.nurture_tasks import run_nurture

__all__ = ["run_nurture"]
