"""Key-values da g-tag: o buffer da api vira valores predefinidos no GAM."""

from types import SimpleNamespace
from typing import Any, cast

import pytest
from avant_core.gam.client.errors import GamError
from avant_core.gam.networks.enums import NetworkStatus
from googleads import errors
from sqlalchemy import text

from avant_worker.services import Services
from avant_worker.tasks.gam import process_key_values, refresh_key_value_networks
from tests.test_gam_tasks import company, network
from tests.test_gam_tool_tasks import soap_writer

KEY_IDS = {"utm_source": "11", "land_uri": "12"}


def _fault(*refused: tuple[int, str]) -> errors.GoogleAdsServerFault:
    """A falha do SOAP com os itens recusados (índice e motivo)."""
    found = [
        SimpleNamespace(reason=reason, fieldPath=f"values[{index}].name")
        for index, reason in refused
    ]
    return errors.GoogleAdsServerFault(None, errors=found, message="recusado")


def test_the_writer_drops_refused_values_and_sends_the_rest_again() -> None:
    writer, client = soap_writer({})
    sent: list[list[str]] = []
    replies = [_fault((0, "VALUE_NAME_DUPLICATE"), (1, "OUTRO_MOTIVO")), None]

    def create(values: list[dict[str, Any]]) -> None:
        """Registra o lote e responde na ordem: primeiro recusa, depois aceita."""
        sent.append([value["name"] for value in values])
        reply = replies.pop(0)
        if reply is not None:
            raise reply

    service = client.GetService("CustomTargetingService", "v202508")
    service.createCustomTargetingValues = create  # type: ignore[attr-defined]
    client.GetService = lambda name, version: service  # type: ignore[method-assign]
    assert writer.ensure_key_values("2100", "11", ["dup", "ruim", "ok"]) == ["dup", "ok"]
    assert sent == [["dup", "ruim", "ok"], ["ok"]]


def test_the_writer_lets_other_gam_errors_through() -> None:
    writer, client = soap_writer({})

    def create(values: list[dict[str, Any]]) -> None:
        """O GAM falha sem apontar item (cota)."""
        raise errors.GoogleAdsServerFault(
            None, errors=[SimpleNamespace(reason="EXCEEDED_QUOTA", fieldPath="")], message="cota"
        )

    service = client.GetService("CustomTargetingService", "v202508")
    service.createCustomTargetingValues = create  # type: ignore[attr-defined]
    client.GetService = lambda name, version: service  # type: ignore[method-assign]
    with pytest.raises(GamError):
        writer.ensure_key_values("2100", "11", ["ok"])


class FakeTrafficWriter:
    """O GAM em memória para as tarefas: as keys da network e os valores criados."""

    def __init__(self) -> None:
        self.created: list[tuple[str, str, str]] = []
        self.key_lookups = 0

    def custom_keys(self, network_code: str, names: list[str]) -> dict[str, str]:
        """Os ids das keys que existem na network."""
        self.key_lookups += 1
        return {name: key_id for name, key_id in KEY_IDS.items() if name in names}

    def ensure_key_values(self, network_code: str, key_id: str, values: list[str]) -> list[str]:
        """Cria e devolve todos."""
        self.created += [(network_code, key_id, value) for value in values]
        return values


@pytest.fixture
def redis_services(services: Services) -> Services:
    """Os serviços com Redis (as tarefas não fazem nada sem ele)."""
    if services.redis is None:
        pytest.skip("defina AVANT_TEST_REDIS_URL")
    return services


def test_buffered_values_become_gam_values_once(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    fake = FakeTrafficWriter()
    services._gam_writer = fake  # type: ignore[assignment]
    services.redis.sadd("kv:buffer:2100", "utm_source:fb", "land_uri:/a", "utm_medium:cpc")
    services.redis.sadd("kv:buffer:networks", "2100")
    assert process_key_values.delay().get() == 2
    assert sorted(fake.created) == [("2100", "11", "fb"), ("2100", "12", "/a")]
    assert not services.redis.exists("kv:buffer:2100")
    assert services.redis.zscore("kv:seen:2100", "utm_source:fb") is not None
    with services.engine.connect() as conn:
        conn.execute(text("SELECT set_config('app.bypass_rls', 'on', false)"))
        rows = conn.execute(text("SELECT key, value FROM gam_key_values ORDER BY key")).all()
    assert [tuple(row) for row in rows] == [("land_uri", "/a"), ("utm_source", "fb")]

    services.redis.sadd("kv:buffer:2100", "utm_source:fb")
    services.redis.sadd("kv:buffer:networks", "2100")
    assert process_key_values.delay().get() == 0
    assert len(fake.created) == 2
    assert fake.key_lookups == 1


def test_connected_networks_reach_the_route(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    services.settings.gam_groone_network_code = "22893970961"
    owner = company(services)
    connected = network(services, owner, code="2100")
    network(services, owner, code="2200")
    with services.trusted_uow() as uow:
        stored = uow.networks.get(connected.id)
        assert stored is not None
        stored.status = NetworkStatus.CONNECTED
        uow.commit()
    assert refresh_key_value_networks.delay().get() == 2
    connected_codes = cast(set[bytes], services.redis.smembers("kv:networks:connected"))
    members = {item.decode() for item in connected_codes}
    assert members == {"2100", "22893970961"}


def test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(
    redis_services: Services,
) -> None:
    services = redis_services
    assert services.redis is not None
    fake = FakeTrafficWriter()
    services._gam_writer = fake  # type: ignore[assignment]
    services.redis.sadd("kv:buffer:2100", "utm_medium:cpc")
    services.redis.sadd("kv:buffer:networks", "2100")
    assert process_key_values.delay().get() == 0
    assert services.redis.zscore("kv:seen:2100", "utm_medium:cpc") is None

    def broken(network_code: str, key_id: str, values: list[str]) -> list[str]:
        """O GAM fora do ar."""
        raise GamError("GAM fora do ar")

    fake.ensure_key_values = broken  # type: ignore[method-assign]
    services.redis.sadd("kv:buffer:2100", "utm_source:raro")
    services.redis.sadd("kv:buffer:networks", "2100")
    assert process_key_values.delay().get() == 0
    pending = cast(set[bytes], services.redis.smembers("kv:buffer:2100"))
    assert pending == {b"utm_source:raro"}
    assert services.redis.sismember("kv:buffer:networks", "2100")
    assert services.redis.zscore("kv:seen:2100", "utm_source:raro") is None
