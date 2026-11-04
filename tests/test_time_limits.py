"""Toda tarefa termina antes de a trava vencer e antes do prazo de ack do RabbitMQ."""

import importlib
from typing import Any
from unittest.mock import patch

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.checklists import checklist_tasks

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


def test_checklists_are_spread_by_rate_limit_not_long_countdowns(services: Services) -> None:
    assert checklist_tasks.check_checklist.rate_limit
    with (
        patch.object(checklist_tasks.check_checklist, "apply_async") as sent,
        patch.object(checklist_tasks, "open_checklist_month", return_value=["a", "b", "c"]),
    ):
        checklist_tasks.open_checklists.run()
    assert all("countdown" not in call.kwargs for call in sent.call_args_list)
    assert app.conf.worker_max_memory_per_child
