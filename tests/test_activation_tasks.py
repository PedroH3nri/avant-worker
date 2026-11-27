"""Funil de ativação: a tarefa diária grava o lead do HubSpot e o cliente, e não duplica."""

from datetime import timedelta

from avant_core.hubspot.errors import HubspotUnavailable
from avant_core.hubspot.models import HubspotLead

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.activation import record_activation
from tests.test_hubspot_tasks import _client


class LeadsHubspot:
    """Um HubSpot que só sabe listar leads, ou falha."""

    def __init__(self, leads: list[HubspotLead], fail: bool = False) -> None:
        self.leads = leads
        self.fail = fail

    def leads_since(self, since: object) -> list[HubspotLead]:
        """Os leads do teste, ou a falha do HubSpot."""
        if self.fail:
            raise HubspotUnavailable("fora do ar")
        return self.leads


def test_activation_records_leads_and_clients_once(services: Services) -> None:
    client_id = _client(services)
    created = services.clock.now() - timedelta(days=3)
    services._hubspot = LeadsHubspot([HubspotLead("501", "lead@novo.com", "Lead", created)])  # type: ignore[assignment]
    first = record_activation.delay().get()
    assert first["leads"] == 1 and first["clients"] >= 1 and first["changed"] >= 2
    assert record_activation.delay().get()["changed"] == 0
    with services.trusted_uow() as uow:
        rows = {item.client_id or item.hubspot_id: item for item in uow.activation_milestones.all()}
    assert rows["501"].lead_on is not None and client_id in rows

    services._hubspot = LeadsHubspot([], fail=True)  # type: ignore[assignment]
    assert record_activation.delay().get()["hubspot_failed"] is True
    services._hubspot = None
    assert record_activation.delay().get()["leads"] == 0


def test_activation_runs_daily_at_05_45() -> None:
    entry = app.conf.beat_schedule["activation"]
    assert entry["task"] == "avant.default.record_activation_milestones"
    assert entry["schedule"].hour == {5} and entry["schedule"].minute == {45}
