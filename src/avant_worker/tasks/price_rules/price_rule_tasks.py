"""Tarefas das regras de preço (decisão 14 do avant-core).

- ``schedule_price_rule_hours`` (minuto 55): para cada network com site de regra ligada,
  ``sync_price_rule_hours`` baixa o relatório por hora da key ``content_hash`` de ontem e de
  hoje, na moeda da network (sem conversão), e troca as linhas na ``gam_key_value_hourly``.
- ``run_price_rules`` (minuto 58): roda o motor em cada site com a regra ligada e apaga o cache
  dos floors dos hashes que mudaram (``avant:price-floors:{site}:{hash}``, que a api lê).
- ``create_price_rules`` (04:00): cria as regras novas dos blocos marcados.
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
from avant_core.metrics.services import maintain_key_value_hourly_partitions
from avant_core.price_rules.catalog import FLOOR_CACHE_KEY
from avant_core.price_rules.services import (
    active_price_rule_sites,
    create_site_price_rules,
    price_rule_networks,
    run_site_price_rules,
    store_price_rule_hours,
)

from avant_worker.adapters.gam_reports import ReportKind
from avant_worker.app import app
from avant_worker.services import Services, get_services

log = logging.getLogger("avant.worker.price_rules")

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
CURRENCY_CACHE = "avant:gam:currency:{network}"
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
            currency = _currency(services, network.network_code)
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


def _currency(services: Services, network_code: str) -> str:
    """A moeda da network no GAM, guardada por um dia no Redis (só leitura no GAM)."""
    key = CURRENCY_CACHE.format(network=network_code)
    if services.redis is not None:
        cached = services.redis.get(key)
        if isinstance(cached, bytes):
            return cached.decode()
    currency = services.gam_writer.target_network(network_code).currency_code
    if services.redis is not None and currency:
        services.redis.set(key, currency, ex=CURRENCY_CACHE_SECONDS)
    return currency


def _forget_floors(services: Services, site_id: uuid.UUID, hashes: list[str]) -> None:
    """Apaga o cache dos floors dos hashes que mudaram; sem Redis, nada a fazer."""
    if services.redis is None or not hashes:
        return
    services.redis.delete(
        *(FLOOR_CACHE_KEY.format(site_id=site_id, content_hash=value) for value in hashes)
    )
