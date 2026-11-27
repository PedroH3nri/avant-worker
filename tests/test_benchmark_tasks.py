"""Comparativo com a rede: a tarefa diária troca os grupos e pode rodar de novo."""

from decimal import Decimal

from avant_core.benchmark.enums import BenchmarkMetric
from avant_core.benchmark.models import BenchmarkGroup
from avant_core.gam.inventory.enums import SiteCategory

from avant_worker.services import Services
from avant_worker.tasks.benchmark import record_benchmark


def test_benchmark_replaces_groups(services: Services) -> None:
    """A rodada apaga o grupo antigo e dá o mesmo resultado ao rodar de novo."""
    with services.trusted_uow() as uow:
        uow.benchmark_groups.replace(
            [
                BenchmarkGroup(
                    "XX", SiteCategory.FOOD, BenchmarkMetric.ECPM, Decimal(1), Decimal(2), 5
                )
            ]
        )
        uow.commit()
    first = record_benchmark.delay().get()
    assert record_benchmark.delay().get() == first
    with services.trusted_uow() as uow:
        stored = uow.benchmark_groups.for_category(SiteCategory.FOOD)
    assert all(group.country != "XX" for group in stored)
