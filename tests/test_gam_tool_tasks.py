import uuid
from typing import Any

import pytest
from avant_core.access.enums import SiteScope
from avant_core.access.models import Actor, Grants
from avant_core.company.models import Company, Membership
from avant_core.gam.inventory.models import Site
from avant_core.gam.tools.enums import GamFormat, GamRunState, GamToolKind
from avant_core.gam.tools.models import BlockSpec, GamOrderRef, GamTargetNetwork, LineItemSpec
from avant_core.gam.tools.services import start_gam_tool
from avant_core.identity.models import User

from avant_worker.adapters.gam_writer import SoapGamWriter, _ad_unit, _line_item
from avant_worker.app import _route, app
from avant_worker.services import Services
from avant_worker.tasks.gam import run_tool, tool_tasks
from tests.test_gam_tasks import company, network


class MemoryWriter:
    """GAM em memória com o mínimo para a configuração completa."""

    def __init__(self) -> None:
        self.created: list[str] = []
        self.items: dict[str, str] = {}
        self.values: dict[str, list[str]] = {}

    def target_network(self, network_code: str) -> GamTargetNetwork:
        """Moeda e raiz."""
        return GamTargetNetwork(network_code, "USD", "root")

    def seller_id(self, child_network_code: str, groone_network_code: str) -> str | None:
        """Seller fixo."""
        return "pub-77"

    def custom_keys(self, network_code: str, names: list[str]) -> dict[str, str]:
        """Nenhuma key."""
        return {}

    def create_custom_keys(self, network_code: str, names: list[str]) -> dict[str, str]:
        """Cria as keys."""
        self.created.append("keys")
        return {name: f"k-{name}" for name in names}

    def create_key_values(self, network_code: str, key_id: str, values: list[str]) -> int:
        """Cria os valores."""
        self.created.append("values")
        self.values[key_id] = values
        return len(values)

    def ensure_key_values(self, network_code: str, key_id: str, values: list[str]) -> list[str]:
        """Cria os valores do tráfego."""
        self.created.append("traffic_values")
        return values

    def find_order(self, network_code: str, name: str) -> GamOrderRef | None:
        """Sem order."""
        return None

    def create_order(self, network_code: str, name: str) -> GamOrderRef:
        """Cria a order."""
        self.created.append("order")
        return GamOrderRef("o1", "a1", approved=False)

    def find_parent_ad_unit(self, network_code: str, domain: str) -> str | None:
        """Sem bloco pai."""
        return None

    def create_parent_ad_unit(self, network_code: str, domain: str, root_id: str) -> str:
        """Cria o bloco pai."""
        self.created.append("parent")
        return "p1"

    def child_ad_units(self, network_code: str, parent_id: str) -> dict[str, str]:
        """Sem filhos."""
        return {}

    def create_child_ad_units(
        self, network_code: str, parent_id: str, blocks: list[BlockSpec]
    ) -> dict[str, str]:
        """Cria os filhos."""
        self.created.append("children")
        return {block.name: f"c-{index}" for index, block in enumerate(blocks)}

    def line_items(self, network_code: str, names: list[str]) -> dict[str, str]:
        """Os line items criados."""
        return {name: self.items[name] for name in names if name in self.items}

    def create_line_items(
        self, network_code: str, order_id: str, items: list[LineItemSpec]
    ) -> dict[str, str]:
        """Cria os line items."""
        self.created.append("line_items")
        self.items.update({item.name: f"l-{item.name}" for item in items})
        return {item.name: f"l-{item.name}" for item in items}

    def add_line_item_targets(
        self, network_code: str, line_item_id: str, ad_unit_ids: list[str]
    ) -> int:
        """Nada novo."""
        return 0

    def find_creative(self, network_code: str, advertiser_id: str) -> str | None:
        """Sem criativo."""
        return None

    def create_creative(self, network_code: str, advertiser_id: str) -> str:
        """Cria o criativo."""
        self.created.append("creative")
        return "cr1"

    def associate_creative(
        self, network_code: str, creative_id: str, line_item_ids: list[str]
    ) -> int:
        """Liga o criativo."""
        self.created.append("association")
        return len(line_item_ids)

    def approve_order(self, network_code: str, order_id: str) -> bool:
        """Aprova."""
        self.created.append("approve")
        return True


def staff(services: Services) -> Actor:
    """A Company Groone com uma pessoa que pode rodar as ferramentas."""
    user = User(email=f"ana-{uuid.uuid4().hex[:6]}@groone.com", name="Ana")
    groone = Company("Groone", user.id, None, f"groone-{uuid.uuid4().hex[:6]}", is_internal=True)
    with services.trusted_uow() as uow:
        uow.users.add(user)
        uow.companies.add(groone)
        uow.memberships.add(Membership(groone.id, user.id, None, services.clock.now()))
        uow.commit()
    permissions = frozenset({"internal.gam_tools.view", "internal.gam_tools.run"})
    return Actor(user.id, groone.id, Grants(permissions, SiteScope.ALL))


def test_tool_task_is_registered() -> None:
    app.loader.import_default_modules()
    assert _route("avant.gam.run_tool") == {"queue": "gam"}


def test_run_tool_configures_the_network(services: Services) -> None:
    writer = MemoryWriter()
    services._gam_writer = writer
    services.settings.gam_groone_network_code = "9999"
    actor = staff(services)
    client = company(services)
    net = network(services, client)
    with services.uow(client.id) as uow:
        uow.sites.add(
            Site(
                client.id,
                "acai.com.br",
                network_id=net.id,
                gam_site_id="s1",
                synced_at=services.clock.now(),
            )
        )
        uow.commit()
    run = start_gam_tool(
        services.trusted_uow(),
        actor=actor,
        network_id=net.id,
        kind=GamToolKind.CONFIG,
        clock=services.clock,
        domains=["acai.com.br"],
        block_format=GamFormat.LIGHT,
    )
    result = run_tool.delay(str(run.id)).get()
    assert result == {"state": "done", "error": None}
    first_steps = [step for step in writer.created if step != "values"][:2]
    assert first_steps == ["keys", "order"] and writer.created[-1] == "approve"
    assert len(writer.values["k-groone_prices"]) == 200
    assert writer.values["k-groone_prices"][:2] == ["0.50", "0.52"]
    assert writer.values["k-groone_group"] == ["regra", "controle"]
    with services.trusted_uow() as uow:
        stored = uow.gam_tool_runs.get(run.id)
        saved = uow.networks.get(net.id)
    assert stored is not None and stored.state is GamRunState.DONE
    assert saved is not None and saved.seller_id == "pub-77"
    assert run_tool.delay(str(run.id)).get() == {"skipped": "not_running"}


class FakeSoapService:
    """Um serviço SOAP que devolve respostas prontas e guarda as chamadas."""

    def __init__(self, calls: list[tuple[str, Any]], replies: dict[str, Any]) -> None:
        self.calls, self.replies = calls, replies

    def __getattr__(self, method: str) -> Any:
        """Qualquer método: registra e devolve a resposta cadastrada."""

        def call(*args: Any) -> Any:
            """Registra a chamada."""
            self.calls.append((method, args))
            return self.replies.get(method)

        return call


class FakeSoapClient:
    """O cliente do googleads com os serviços falsos."""

    def __init__(self, replies: dict[str, Any]) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.replies = replies

    def GetService(self, name: str, version: str) -> FakeSoapService:
        """O serviço pedido."""
        return FakeSoapService(self.calls, self.replies)


def soap_writer(replies: dict[str, Any]) -> tuple[SoapGamWriter, FakeSoapClient]:
    """Um SoapGamWriter que fala com o cliente falso."""
    writer = SoapGamWriter("chave.json", version="v202508")
    client = FakeSoapClient(replies)
    writer._client = lambda network_code: client  # type: ignore[method-assign]
    return writer, client


def test_writer_payloads_follow_genius() -> None:
    unit = _ad_unit(
        "p1", BlockSpec("Acai_Offerwall_20261104", "Offerwall", ((300, 250),), True, True)
    )
    assert unit["targetWindow"] == "TOP" and unit["adUnitCode"] == unit["name"]
    assert unit["isInterstitial"] and unit["isFluid"]
    assert unit["adUnitSizes"][0]["environmentType"] == "BROWSER"
    item = _line_item("10", LineItemSpec("Display", ("root",), True, "BRL", "ca-pub-1"))
    assert item["lineItemType"] == "AD_EXCHANGE" and item["costPerUnit"]["microAmount"] == 0
    assert item["creativePlaceholders"][0]["creativeSizeType"] == "IGNORED"
    assert item["targeting"]["inventoryTargeting"]["targetedAdUnits"][0]["includeDescendants"]


def test_writer_skips_what_already_exists() -> None:
    order = {"id": 5, "advertiserId": 6, "status": "APPROVED"}
    line_item = {
        "id": 7,
        "targeting": {"inventoryTargeting": {"targetedAdUnits": [{"adUnitId": "a"}]}},
    }
    writer, client = soap_writer(
        {
            "getOrdersByStatement": {"results": [order]},
            "getLineItemsByStatement": {"results": [line_item]},
        }
    )
    assert writer.approve_order("1", "5") is False
    assert writer.add_line_item_targets("1", "7", ["a"]) == 0
    assert writer.add_line_item_targets("1", "7", ["a", "b"]) == 1
    methods = [method for method, _args in client.calls]
    assert "performOrderAction" not in methods and methods.count("updateLineItems") == 1


@pytest.mark.parametrize("seller", ["pub-9", None])
def test_writer_reads_seller_in_groone_network(seller: str | None) -> None:
    company_row = {"childPublisher": {"sellerId": seller}}
    writer, _client = soap_writer({"getCompaniesByStatement": {"results": [company_row]}})
    assert writer.seller_id("123", "9999") == seller


def test_a_busy_network_waits_and_tries_again(services: Services, monkeypatch: Any) -> None:
    services.settings.gam_groone_network_code = "9999"
    actor = staff(services)
    client = company(services)
    net = network(services, client)
    run = start_gam_tool(
        services.trusted_uow(),
        actor=actor,
        network_id=net.id,
        kind=GamToolKind.SYNC,
        clock=services.clock,
    )
    later: list[tuple[str, int]] = []
    monkeypatch.setattr(
        tool_tasks, "_try_later", lambda run_id, attempt: later.append((run_id, attempt))
    )
    held = services.redis.lock(f"avant:lock:gam:tool:network:{net.id}", timeout=60, blocking=False)
    assert held.acquire()
    try:
        assert run_tool.delay(str(run.id)).get() == {"skipped": "network_busy"}
    finally:
        held.release()
    assert later == [(str(run.id), 1)]
