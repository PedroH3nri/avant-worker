import uuid
from typing import Any

import pytest
from avant_core.company.domain import Company, CompanyPlan
from avant_core.gam.domain import (
    ConnectionType,
    Delegation,
    InventoryStatus,
    Network,
    NetworkStatus,
)
from avant_core.identity.domain import User
from avant_core.ports import (
    GamAccessDenied,
    GamAdUnit,
    GamChildPublisher,
    GamNetworkInfo,
    GamSite,
    GamUnavailable,
)
from sqlalchemy import text

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.gam import (
    check_access,
    discover_mcm,
    schedule_imports,
    schedule_tests,
    sync_network,
)
from tests.conftest import GROONE_NETWORK
from tests.fake_gam import FakeGamClient


def fake(services: Services) -> FakeGamClient:
    client = services.gam.client
    assert isinstance(client, FakeGamClient)
    return client


def company(services: Services, email: str = "dono@acai.com.br") -> Company:
    user = User(email=email, name="Dono")
    c = Company(
        name="Açaí",
        owner_user_id=user.id,
        seat_limit=3,
        plan=CompanyPlan.EXTERNAL,
        slug=f"acai-{uuid.uuid4().hex[:6]}",
    )
    with services.trusted_uow() as uow:
        uow.users.add(user)
        uow.companies.add(c)
        uow.commit()
    return c


def network(services: Services, c: Company, code: str = "123") -> Network:
    n = Network(
        company_id=c.id,
        network_code=code,
        connection_type=ConnectionType.SERVICE_ACCOUNT,
        created_at=services.clock.now(),
    )
    with services.uow(c.id) as uow:
        uow.networks.add(n)
        uow.commit()
    return n


def inventory(client: FakeGamClient, code: str = "123") -> None:
    client.networks[code] = GamNetworkInfo(code, "Açaí", is_test=False)
    client.admin_of.add(code)
    client.sites[code] = [GamSite("s1", "https://www.acai.com.br/", "APPROVED")]
    client.ad_units[code] = [
        GamAdUnit("u1", None, "acai.com.br", None, InventoryStatus.ACTIVE),
        GamAdUnit("u2", "u1", "topo", "acai_topo", InventoryStatus.ACTIVE),
    ]


def count(services: Services, table: str) -> int:
    with services.trusted_uow() as uow:
        return int(uow.session.execute(text(f"SELECT count(*) FROM {table}")).scalar_one())


def test_gam_tasks_are_registered_on_the_gam_queue() -> None:
    from avant_worker.app import _route

    app.loader.import_default_modules()
    for name in (
        "avant.gam.sync_network",
        "avant.gam.check_access",
        "avant.gam.discover_mcm",
        "avant.gam.schedule_tests",
        "avant.gam.schedule_imports",
    ):
        assert name in app.tasks and _route(name) == {"queue": "gam"}
    # 1, 2, 4 e 8 minutos em erro temporário.
    task: Any = sync_network
    assert task.autoretry_for == (GamUnavailable,)
    assert task.max_retries == 4 and task.retry_backoff == 60


def test_sync_network_tests_then_imports(services: Services) -> None:
    c = company(services)
    n = network(services, c)
    inventory(fake(services))

    result = sync_network.delay(str(c.id), str(n.id)).get()
    assert result["test"] == {"ok": True, "status": "connected"}
    assert result["sites"] == {"created": 1, "updated": 0, "archived": 0}
    assert result["ad_units"]["created"] == 2 and result["ad_units"]["without_site"] == 0
    with services.uow(c.id) as uow:
        (site,) = uow.sites.list_for_network(n.id)
        assert site.domain == "acai.com.br"
        assert {u.site_id for u in uow.ad_units.list_for_network(n.id)} == {site.id}

    # De novo (o agendador, sem teste): upsert, nada duplicado.
    again = sync_network.delay(str(c.id), str(n.id), test=False).get()
    assert "test" not in again and again["sites"]["updated"] == 1
    assert count(services, "sites") == 1 and count(services, "ad_units") == 2


def test_failed_check_stops_before_importing(services: Services) -> None:
    c = company(services)
    n = network(services, c)
    client = fake(services)
    inventory(client)
    client.admin_of.clear()

    result = sync_network.delay(str(c.id), str(n.id)).get()
    assert result == {"test": {"ok": False, "status": "error"}}
    assert ("list_sites", "123") not in client.calls
    with services.uow(c.id) as uow:
        saved = uow.networks.get(n.id)
        assert saved is not None and saved.last_error == "gam_not_admin"


def test_permanent_error_during_import_is_recorded_not_retried(services: Services) -> None:
    c = company(services)
    n = network(services, c)
    client = fake(services)
    inventory(client)
    # Passa no teste (get_network e is_admin) e falha ao ler os sites.
    client.fail_next["123"] = []
    sync_network.delay(str(c.id), str(n.id)).get()
    client.fail_next["123"] = [GamAccessDenied("403")]

    result = sync_network.delay(str(c.id), str(n.id), test=False).get()
    assert result == {"error": "gam_access_denied"}
    with services.uow(c.id) as uow:
        saved = uow.networks.get(n.id)
        assert saved is not None and saved.failures == 1
        assert saved.status is NetworkStatus.CONNECTED  # só vira erro na terceira


def test_check_access_and_schedulers(services: Services) -> None:
    c = company(services)
    n = network(services, c)
    inventory(fake(services))

    assert check_access.delay(str(c.id), str(n.id)).get() == {
        "ok": True,
        "status": "connected",
        "error": None,
    }
    assert schedule_tests.delay().get() == 1
    assert schedule_imports.delay().get() == 1
    assert count(services, "sites") == 1


def test_discover_mcm_creates_network_and_imports(services: Services) -> None:
    c = company(services, "dono@acai.com.br")
    client = fake(services)
    client.networks[GROONE_NETWORK] = GamNetworkInfo(GROONE_NETWORK, "Groone", is_test=False)
    client.children = [
        GamChildPublisher(
            network_code="123",
            display_name="Açaí",
            email="dono@acai.com.br",
            delegation=Delegation.MANAGE_INVENTORY,
            account_status="APPROVED",
        ),
        GamChildPublisher("456", None, "ninguem@x.com", Delegation.MANAGE_ACCOUNT, "APPROVED"),
    ]
    # Manage Inventory: os sites e ad units estão na network da Groone.
    client.sites[GROONE_NETWORK] = [
        GamSite("s1", "acai.com.br", "APPROVED", child_network_code="123"),
        GamSite("s9", "outro.com", "APPROVED", child_network_code="777"),
    ]
    client.ad_units[GROONE_NETWORK] = [
        GamAdUnit("u1", None, "acai.com.br", None, InventoryStatus.ACTIVE),
        GamAdUnit("u9", None, "outro.com", None, InventoryStatus.ACTIVE),
    ]

    assert discover_mcm.delay().get() == {
        "created": 1,
        "candidates": 1,
        "disconnected": 0,
        "updated": 0,
    }
    with services.uow(c.id) as uow:
        (n,) = uow.networks.list_for_company(c.id)
        assert n.connection_type is ConnectionType.MCM and n.status is NetworkStatus.CONNECTED
        assert [s.domain for s in uow.sites.list_for_network(n.id)] == ["acai.com.br"]
        assert len(uow.ad_units.list_for_network(n.id)) == 1
    assert count(services, "mcm_candidates") == 1


def test_lock_skips_a_second_run(services: Services) -> None:
    if services.redis is None:
        pytest.skip("defina AVANT_TEST_REDIS_URL")
    c = company(services)
    n = network(services, c)
    inventory(fake(services))
    with services.lock(f"gam:network:{n.id}", timeout=60) as locked:
        assert locked
        assert sync_network.delay(str(c.id), str(n.id)).get() == {"skipped": "locked"}
    assert sync_network.delay(str(c.id), str(n.id)).get()["test"]["ok"]


def test_sync_publishes_network_events(services: Services) -> None:
    if services.redis is None:
        pytest.skip("defina AVANT_TEST_REDIS_URL")
    import json

    from avant_worker.events import channel

    c = company(services)
    n = network(services, c)
    inventory(fake(services))
    pubsub = services.redis.pubsub()  # type: ignore[no-untyped-call]
    pubsub.subscribe(channel(c.id))
    pubsub.get_message(timeout=1)  # confirmação da inscrição

    sync_network.delay(str(c.id), str(n.id)).get()
    events = []
    while (message := pubsub.get_message(timeout=0.5)) is not None:
        events.append(json.loads(message["data"]))
    pubsub.close()
    # Teste, sites e ad units: a tela busca o estado de novo a cada aviso.
    assert events == [{"type": "network.updated", "data": {"network_id": str(n.id)}}] * 3


def test_publish_without_redis_is_a_no_op() -> None:
    from avant_worker.events import publish

    publish(None, uuid.uuid4(), "network.updated", {"network_id": "x"})
