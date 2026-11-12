"""Tarefas das regras de preço (decisão 14 do avant-core).

- ``schedule_price_rule_hours`` (minuto 55): para cada network com site de regra ligada,
  ``sync_price_rule_hours`` baixa o relatório por hora das keys ``content_hash`` e
  ``groone_try`` de ontem e de hoje, na moeda da network (sem conversão), e troca as linhas na
  ``gam_key_value_hourly`` numa chamada só. Também grava o fuso da network (``timeZone`` do
  ``getCurrentNetwork``), que o motor usa para o floor por hora da Cascata.
- ``run_price_rules`` (minuto 58): roda o motor em cada site com a regra ligada e apaga o cache
  dos floors dos hashes que mudaram (``avant:price-floors:{site}:{hash}``, que a api lê). Depois
  roda a Cascata do site e, se algum floor inicial mudou, apaga ``avant:price-cascades:{site}``.
- ``create_price_rules`` (04:00): cria as regras novas dos blocos marcados e as Cascatas.
- ``maintain_price_rule_partitions`` (diária): partições da tabela por hora, 30 dias.

Networks do MCM Manage Inventory ficam de fora: o inventário delas está na network da Groone.
Os ``schedule``, o motor e a criação usam ``trusted_uow``; a gravação usa a Empresa da network.
"""

import logging
import uuid
from datetime import timedelta
from zoneinfo import ZoneInfo

from avant_core.gam.client.errors import GamError, GamUnavailable
from avant_core.gam.networks.enums import ConnectionType, Delegation
from avant_core.gam.networks.models import Network
from avant_core.gam.networks.services import record_network_time_zone
from avant_core.metrics.services import maintain_key_value_hourly_partitions
from avant_core.price_rules.catalog import CASCADE_CACHE_KEY, FLOOR_CACHE_KEY
from avant_core.price_rules.services import (
    active_price_rule_sites,
    create_site_cascades,
    create_site_price_rules,
    price_rule_networks,
    run_site_cascades,
    run_site_price_rules,
    store_price_rule_hours,
)

from avant_worker.adapters.gam_reports import ReportKind
from avant_worker.adapters.gam_writer import GamTargetNetworkWithTimeZone
from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.price_rules")

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
CURRENCY_CACHE = "avant:gam:currency:{network}"
TIME_ZONE_CACHE = "avant:gam:time-zone:{network}"
CURRENCY_CACHE_SECONDS = 24 * 60 * 60
LOCK_SECONDS = 15 * 60
SOFT_LIMIT_SECONDS = 12 * 60
HARD_LIMIT_SECONDS = 14 * 60


@app.task(
    name="avant.gam.schedule_price_rule_hours",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def schedule_price_rule_hours() -> int:
    """De hora em hora: agenda a sincronia por hora de cada network com regra ligada."""
    networks = price_rule_networks(get_services().trusted_uow())
    for company_id, network_id in networks:
        sync_price_rule_hours.delay(str(company_id), str(network_id))
    return len(networks)


@app.task(
    name="avant.gam.sync_price_rule_hours",
    autoretry_for=(GamUnavailable,),
    retry_backoff=60,
    retry_backoff_max=4 * 60,
    retry_jitter=False,
    max_retries=2,
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def sync_price_rule_hours(company_id: str, network_id: str) -> int:
    """Troca as horas de ontem e de hoje da network pelas do GAM; devolve quantas linhas."""
    services = get_services()
    with services.lock(f"gam:price-rule-hours:{network_id}", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        with services.uow(uuid.UUID(company_id)) as uow:
            network = uow.networks.get(uuid.UUID(network_id))
        if network is None or _reads_groone_network(network):
            return 0
        today = services.clock.now().astimezone(SAO_PAULO).date()
        days = [today - timedelta(days=1), today]
        try:
            currency, time_zone = _currency_and_time_zone(services, network.network_code)
            with services.reports.report(
                network.network_code,
                ReportKind.PRICE_RULE_HOURS,
                days[0],
                days[-1],
                currency=currency,
            ) as rows:
                stored = store_price_rule_hours(
                    services.uow(network.company_id),
                    network_id=network.id,
                    rows=rows,
                    currency=currency,
                    days=days,
                    clock=services.clock,
                )
        except GamError as exc:
            if not exc.permanent:
                raise
            log.warning(
                "horas das regras de preço falharam",
                extra={"network_id": network_id, "error": exc.code},
            )
            return 0
        _record_time_zone(services, network, time_zone)
    log.info(
        "horas das regras de preço gravadas",
        extra={"network_id": network_id, "currency": currency, "rows": stored},
    )
    return stored


@app.task(
    name="avant.default.run_price_rules",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def run_price_rules() -> int:
    """De hora em hora: o motor em cada site com regra ligada; um site que falha não para os
    outros. Devolve quantos hashes mudaram de floor."""
    services = get_services()
    changed = 0
    with services.lock("price-rules", timeout=LOCK_SECONDS) as locked:
        if not locked:
            return 0
        for site_id in active_price_rule_sites(services.trusted_uow()):
            try:
                hashes = run_site_price_rules(
                    services.trusted_uow(), site_id=site_id, clock=services.clock
                )
            except Exception:
                log.exception("motor das regras de preço falhou", extra={"site_id": str(site_id)})
                continue
            _forget_floors(services, site_id, hashes)
            changed += len(hashes)
            try:
                start_changed = run_site_cascades(
                    services.trusted_uow(), site_id=site_id, clock=services.clock
                )
            except Exception:
                log.exception("motor da Cascata falhou", extra={"site_id": str(site_id)})
                continue
            if start_changed:
                _forget_cascades(services, site_id)
    return changed


@app.task(
    name="avant.default.create_price_rules",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def create_price_rules() -> int:
    """Uma vez por dia: as regras novas dos blocos marcados (300+ elegíveis ontem)."""
    services = get_services()
    created = 0
    for site_id in active_price_rule_sites(services.trusted_uow()):
        try:
            created += create_site_price_rules(
                services.trusted_uow(), site_id=site_id, clock=services.clock
            )
        except Exception:
            log.exception("criação das regras de preço falhou", extra={"site_id": str(site_id)})
        try:
            created += create_site_cascades(
                services.trusted_uow(), site_id=site_id, clock=services.clock
            )
        except Exception:
            log.exception("criação das Cascatas falhou", extra={"site_id": str(site_id)})
    if created:
        log.info("regras de preço criadas", extra={"rules": created})
    return created


@app.task(
    name="avant.default.maintain_price_rule_partitions",
    soft_time_limit=SOFT_LIMIT_SECONDS,
    time_limit=HARD_LIMIT_SECONDS,
)
def maintain_price_rule_partitions() -> dict[str, int]:
    """Uma vez por dia: cria as partições dos próximos dias e apaga as de mais de 30 dias."""
    services = get_services()
    created, dropped = maintain_key_value_hourly_partitions(
        services.trusted_uow(), clock=services.clock
    )
    return {"created": created, "dropped": dropped}


def _reads_groone_network(network: Network) -> bool:
    """MCM Manage Inventory: o inventário e os relatórios ficam na network da Groone."""
    return (
        network.connection_type is ConnectionType.MCM
        and network.delegation is Delegation.MANAGE_INVENTORY
    )


def _currency_and_time_zone(services: Services, network_code: str) -> tuple[str, str]:
    """A moeda e o fuso da network no GAM, guardados por um dia no Redis; uma só chamada ao
    ``getCurrentNetwork`` quando falta um dos dois (só leitura no GAM)."""
    currency_key = CURRENCY_CACHE.format(network=network_code)
    time_zone_key = TIME_ZONE_CACHE.format(network=network_code)
    cached_currency = services.redis.get(currency_key)
    cached_time_zone = services.redis.get(time_zone_key)
    if isinstance(cached_currency, bytes) and isinstance(cached_time_zone, bytes):
        return cached_currency.decode(), cached_time_zone.decode()
    target = services.gam_writer.target_network(network_code)
    time_zone = target.time_zone if isinstance(target, GamTargetNetworkWithTimeZone) else ""
    if target.currency_code:
        services.redis.set(currency_key, target.currency_code, ex=CURRENCY_CACHE_SECONDS)
        services.redis.set(time_zone_key, time_zone, ex=CURRENCY_CACHE_SECONDS)
    return target.currency_code, time_zone


def _record_time_zone(services: Services, network: Network, time_zone: str) -> None:
    """Grava o fuso da network; qualquer falha é registrada e a sincronia segue."""
    if not time_zone:
        return
    try:
        record_network_time_zone(services.trusted_uow(), network_id=network.id, time_zone=time_zone)
    except Exception:
        log.warning(
            "fuso da network não gravado",
            extra={"network_id": str(network.id), "time_zone": time_zone},
        )


def _forget_floors(services: Services, site_id: uuid.UUID, hashes: list[str]) -> None:
    """Apaga o cache dos floors dos hashes que mudaram."""
    if not hashes:
        return
    services.redis.delete(
        *(FLOOR_CACHE_KEY.format(site_id=site_id, content_hash=value) for value in hashes)
    )


def _forget_cascades(services: Services, site_id: uuid.UUID) -> None:
    """Apaga o cache das Cascatas do site, que a api lê."""
    services.redis.delete(CASCADE_CACHE_KEY.format(site_id=site_id))
