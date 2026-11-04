"""Toda tarefa termina antes de a trava vencer e antes do prazo de ack do RabbitMQ."""

import importlib
import uuid
from typing import Any
from unittest.mock import patch

import pytest
from celery.exceptions import SoftTimeLimitExceeded

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.checklists import checklist_tasks
from avant_worker.tasks.reports import report_preview_tasks

RABBITMQ_ACK_SECONDS = 30 * 60


def _limits(task: Any) -> tuple[float, float]:
    """O soft e o hard limit da tarefa, ou os globais quando ela não tem os seus."""
    soft = task.soft_time_limit or app.conf.task_soft_time_limit
    hard = task.time_limit or app.conf.task_time_limit
    return soft, hard


def test_every_task_has_limits_below_the_rabbitmq_ack_timeout() -> None:
    for name, task in app.tasks.items():
        if not name.startswith("avant."):
            continue
        soft, hard = _limits(task)
        assert soft and hard and soft < hard < RABBITMQ_ACK_SECONDS, name


def test_tasks_finish_before_their_lock_expires() -> None:
    for name, task in app.tasks.items():
        if not name.startswith("avant."):
            continue
        module = importlib.import_module(task.run.__module__)
        lock = getattr(module, "LOCK_SECONDS", None)
        if lock is None:
            continue
        _, hard = _limits(task)
        assert hard < lock or lock >= RABBITMQ_ACK_SECONDS, (name, hard, lock)


def test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(
    services: Services,
) -> None:
    ids = [str(uuid.uuid4()) for _ in range(30)]
    assert not checklist_tasks.check_checklist.rate_limit
    with (
        patch.object(checklist_tasks.check_checklist, "apply_async") as checks,
        patch.object(checklist_tasks.dispatch_checklists, "apply_async") as later,
        patch.object(checklist_tasks, "open_checklist_month", return_value=ids),
    ):
        checklist_tasks.open_checklists.run()
    countdowns = [call.kwargs["countdown"] for call in checks.call_args_list]
    assert len(countdowns) == checklist_tasks.CHECKS_PER_BATCH and max(countdowns) < 60
    (call,) = later.call_args_list
    assert call.kwargs["args"] == (ids[checklist_tasks.CHECKS_PER_BATCH :],)
    assert call.kwargs["countdown"] == checklist_tasks.BATCH_SECONDS
    assert app.conf.worker_max_memory_per_child


def test_report_previews_stop_at_the_soft_limit(services: Services) -> None:
    with (
        patch.object(report_preview_tasks, "stale_report_ids", return_value=[uuid.uuid4()]),
        patch.object(report_preview_tasks, "refresh_preview", side_effect=SoftTimeLimitExceeded()),
        pytest.raises(SoftTimeLimitExceeded),
    ):
        report_preview_tasks.refresh_report_previews.run()


def test_task_results_are_not_kept_in_redis() -> None:
    assert app.conf.task_ignore_result is True
