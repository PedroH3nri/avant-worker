"""Tarefas das oportunidades de receita."""

from avant_worker.tasks.opportunities.opportunity_tasks import evaluate_site_opportunities

__all__ = ["evaluate_site_opportunities"]
