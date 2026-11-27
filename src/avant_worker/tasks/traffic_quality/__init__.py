"""Tarefas da qualidade do tráfego."""

from avant_worker.tasks.traffic_quality.traffic_quality_tasks import evaluate_traffic_quality

__all__ = ["evaluate_traffic_quality"]
