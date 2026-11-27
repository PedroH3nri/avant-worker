"""Sincronia com o HubSpot no worker: desligada sem token, roda a pedida e grava os vínculos."""

import uuid
from datetime import UTC, datetime, timedelta

from avant_core.company.enums import CompanyStatus
from avant_core.company.models import ClientProfile, Company
from avant_core.gam.networks.enums import ConnectionType, NetworkStatus
from avant_core.gam.networks.models import Network
from avant_core.hubspot.enums import HubspotKind, HubspotRunState
from avant_core.hubspot.errors import HubspotRejected
from avant_core.hubspot.models import (
    HubspotAssociation,
    HubspotCard,
    HubspotLead,
    HubspotLink,
    HubspotProperty,
    HubspotProspectPage,
    HubspotRecord,
    HubspotTaskDraft,
    HubspotWriteResult,
)
from avant_core.hubspot.services import request_hubspot_sync

from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.hubspot import sync_hubspot, sync_hubspot_followups


class FakeHubspot:
    """Um HubSpot em memória que cria tudo com ids novos."""

    def __init__(self, refuse_token: bool = False, custom_objects: bool = True) -> None:
        self.created: list[HubspotRecord] = []
        self.refuse_token = refuse_token
        self.custom_objects = custom_objects
        self.tasks: list[tuple[HubspotTaskDraft, str | None]] = []
        self.done: set[str] = set()

    def portal_id(self) -> str:
        """Portal de teste."""
        return "1"

    def has_object(self, kind: HubspotKind) -> bool:
        """Os personalizados só com a licença."""
        return not kind.custom or self.custom_objects

    def ensure_properties(self, properties: list[HubspotProperty]) -> set[str]:
        """Todas existem; ou o token é recusado."""
        if self.refuse_token:
            raise HubspotRejected("o HubSpot recusou o token do Avant")
        return {prop.name for prop in properties}

    def find(self, kind: HubspotKind, key_property: str, values: list[str]) -> dict[str, str]:
        """Nada existe ainda."""
        return {}

    def create(self, kind: HubspotKind, records: list[HubspotRecord]) -> list[HubspotWriteResult]:
        """Cria com ids sequenciais."""
        self.created.extend(records)
        return [
            HubspotWriteResult(record.avant_id, str(len(self.created) + index))
            for index, record in enumerate(records)
        ]

    def update(
        self, kind: HubspotKind, items: list[tuple[str, HubspotRecord]]
    ) -> list[HubspotWriteResult]:
        """Atualiza todos."""
        return [HubspotWriteResult(record.avant_id, hubspot_id) for hubspot_id, record in items]

    def associate(self, associations: list[HubspotAssociation]) -> None:
        """Não guarda nada."""

    def owners(self) -> dict[str, str]:
        """Sem donos."""
        return {}

    def card(self, kind: HubspotKind, hubspot_id: str) -> HubspotCard:
        """Não usado pelo worker."""
        return HubspotCard(kind, hubspot_id)

    def create_task(self, draft: HubspotTaskDraft, owner_id: str | None) -> str:
        """Cria a tarefa com id sequencial."""
        self.tasks.append((draft, owner_id))
        return f"t{len(self.tasks)}"

    def completed_tasks(self, hubspot_ids: list[str]) -> set[str]:
        """As que o teste marcou como feitas."""
        return {item for item in hubspot_ids if item in self.done}

    def complete_tasks(self, hubspot_ids: list[str]) -> None:
        """Não guarda nada."""

    def prospects(self, stages: list[str], query: str, after: str | None) -> HubspotProspectPage:
        """Não usado pelo worker."""
        return HubspotProspectPage()

    def leads_since(self, since: datetime) -> list[HubspotLead]:
        """Nenhum lead."""
        return []


def _client(services: Services) -> uuid.UUID:
    """Um cliente cadastrado."""
    client_id = uuid.uuid4()
    with services.trusted_uow() as uow:
        uow.client_profiles.add(
            ClientProfile(
                id=client_id,
                first_name="Ana",
                last_name="Hub",
                email=f"ana-{client_id.hex[:8]}@hub.com",
                name="Hub",
                status=CompanyStatus.ACTIVE,
            )
        )
        uow.commit()
    return client_id


def test_hubspot_tasks_go_to_their_queue() -> None:
    """A tarefa vai para a fila hubspot."""
    assert _route("avant.hubspot.sync") == {"queue": "hubspot"}


def test_sync_does_nothing_without_the_token(services: Services) -> None:
    """Sem HUBSPOT_ACCESS_TOKEN a tarefa só volta."""
    services._hubspot = None
    assert sync_hubspot.delay().get() == {"skipped": 1}


def test_sync_runs_the_routine_and_saves_links(services: Services) -> None:
    """A de rotina manda o cliente e grava o vínculo; logo depois não roda de novo."""
    client_id = _client(services)
    fake = FakeHubspot()
    services._hubspot = fake
    result = sync_hubspot.delay().get()
    assert result["changed"] >= 1 and result["failed"] == 0
    assert any(record.avant_id == client_id for record in fake.created)
    with services.trusted_uow() as uow:
        link = uow.hubspot_links.get(HubspotKind.CONTACT, client_id)
        assert link is not None and link.hubspot_id
    assert sync_hubspot.delay().get() == {"skipped": 1}


def test_requested_sync_runs_and_a_refused_token_fails_the_run(services: Services) -> None:
    """O "Sincronizar agora" roda na hora; token recusado fecha a sincronia com o motivo."""
    _client(services)
    services._hubspot = FakeHubspot(refuse_token=True)
    now = datetime.now(UTC)
    with services.trusted_uow() as uow:
        run = request_hubspot_sync(uow, None, now - timedelta(seconds=1), configured=True)  # type: ignore[arg-type]
        uow.commit()
    assert sync_hubspot.delay().get() == {"failed": 1}
    with services.trusted_uow() as uow:
        saved = uow.hubspot_runs.get(run.id)
        assert saved is not None and saved.state is HubspotRunState.FAILED
        assert saved.error == "o HubSpot recusou o token do Avant"


def test_monthly_sync_runs_right_after_the_routine(services: Services) -> None:
    """A mensal do beat não espera os 15 minutos da de rotina; sem a licença, os objetos
    personalizados ficam de fora sem erro."""
    _client(services)
    fake = FakeHubspot(custom_objects=False)
    services._hubspot = fake
    sync_hubspot.delay().get()
    assert sync_hubspot.delay().get() == {"skipped": 1}
    result = sync_hubspot.delay(monthly=True).get()
    assert "failed" in result and result["failed"] == 0
    assert all(not record.kind.custom for record in fake.created)


def test_monthly_sync_is_scheduled_daily() -> None:
    """O beat tem a mensal todo dia, com ``monthly``."""
    entry = app.conf.beat_schedule["hubspot-sync-monthly"]
    assert entry["task"] == "avant.hubspot.sync" and entry["kwargs"] == {"monthly": True}


def test_followups_go_to_the_hubspot_queue_every_15_minutes() -> None:
    """As tarefas do gerente vão para a fila hubspot, a cada 15 minutos."""
    assert _route("avant.hubspot.followups") == {"queue": "hubspot"}
    assert app.conf.beat_schedule["hubspot-followups"]["schedule"] == 900.0


def test_followups_do_nothing_without_the_token(services: Services) -> None:
    """Sem HUBSPOT_ACCESS_TOKEN a tarefa só volta."""
    services._hubspot = None
    assert sync_hubspot_followups.delay().get() == {"skipped": 1}


def test_network_error_becomes_one_task_on_the_client_contact(services: Services) -> None:
    """A network com erro de um cliente já no HubSpot vira uma tarefa, só uma vez."""
    client_id = _client(services)
    company = Company("Hub Tarefas", None, 3, f"hubt-{client_id.hex[:8]}", client_id=client_id)
    network = Network(
        company.id, f"94{client_id.int % 10**6:06d}", ConnectionType.MCM, datetime.now(UTC)
    )
    network.client_id, network.status = client_id, NetworkStatus.ERROR
    with services.trusted_uow() as uow:
        uow.companies.add(company)
        uow.networks.add(network)
        uow.hubspot_links.add(HubspotLink(HubspotKind.CONTACT, client_id, "Ana", hubspot_id="501"))
        uow.commit()
    fake = FakeHubspot()
    services._hubspot = fake
    result = sync_hubspot_followups.delay().get()
    assert result["created"] >= 1
    mine = [draft for draft, _owner in fake.tasks if draft.contact_id == "501"]
    assert len(mine) == 1 and "com erro" in mine[0].subject
    sync_hubspot_followups.delay().get()
    assert len([draft for draft, _owner in fake.tasks if draft.contact_id == "501"]) == 1
