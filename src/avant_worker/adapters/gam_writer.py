"""Escritas no Google Ad Manager pela API SOAP, para as ferramentas do GAM (worker#64).

ESTE É O ÚNICO ARQUIVO DO AVANT QUE ESCREVE NO GAM. Cada método que cria ou altera algo
passa pela revisão do Pedro antes do merge (regra do CLAUDE.md). A API REST v1 não cria
orders, line items nem criativos; por isso é SOAP, com a mesma biblioteca dos relatórios.

O que cada escrita faz é o mesmo do ``AdmanagerService`` do Genius: anunciante "google",
order "AdExchange", blocos com ``targetWindow`` TOP e tamanhos BROWSER, line items Ad
Exchange com CPM zero, criativo "Display All requested sizes" e a aprovação da order. A
diferença é que aqui toda escrita confere antes o que já existe e só cria o que falta.
"""

import logging
import re
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

from avant_core.gam.client.errors import GamAccessDenied, GamError, GamUnavailable
from avant_core.gam.tools.models import BlockSpec, GamOrderRef, GamTargetNetwork, LineItemSpec
from google.auth import exceptions as auth_exceptions
from googleads import ad_manager, errors, oauth2

from avant_worker.adapters.gam_reports import APPLICATION_NAME, _classify

ADVERTISER_NAME = "google"
CREATIVE_NAME = "Display All requested sizes: automatically generated on {moment}"
CREATIVE_SNIPPET = "<!-- Ad Exchange -->"
CREATE_BATCH = 500
DUPLICATE = "VALUE_NAME_DUPLICATE"

log = logging.getLogger("avant.worker.gam")


class SoapGamWriter:
    """Implementa o ``GamWriter`` do avant-core; um cliente do googleads por network."""

    def __init__(self, key_file: str, *, version: str | None = None) -> None:
        self._key_file = key_file
        self._version = version or sorted(ad_manager._SERVICE_MAP)[-1]
        self._oauth: oauth2.GoogleServiceAccountClient | None = None
        self._clients: dict[str, ad_manager.AdManagerClient] = {}

    def target_network(self, network_code: str) -> GamTargetNetwork:
        """Lê a moeda e o bloco raiz da network (só leitura)."""
        network = self._call(network_code, "NetworkService", "getCurrentNetwork")
        return GamTargetNetwork(
            network_code=network_code,
            currency_code=str(network["currencyCode"]),
            root_ad_unit_id=str(network["effectiveRootAdUnitId"]),
        )

    def seller_id(self, child_network_code: str, groone_network_code: str) -> str | None:
        """Lê na network da Groone o seller ID da filha do MCM (só leitura)."""
        statement = self._statement(
            "childNetworkCode = :code", {"code": child_network_code}, limit=1
        )
        found = self._first(
            groone_network_code, "CompanyService", "getCompaniesByStatement", statement
        )
        publisher = found["childPublisher"] if found is not None else None
        seller = publisher["sellerId"] if publisher is not None else None
        return str(seller) if seller else None

    def custom_keys(self, network_code: str, names: list[str]) -> dict[str, str]:
        """As keys de key value com esses nomes que já existem (só leitura)."""
        statement = self._statement("name IN (:names)", {"names": names})
        return {
            str(key["name"]): str(key["id"])
            for key in self._all(
                network_code,
                "CustomTargetingService",
                "getCustomTargetingKeysByStatement",
                statement,
            )
        }

    def create_custom_keys(self, network_code: str, names: list[str]) -> dict[str, str]:
        """ESCREVE: cria as keys predefinidas, ativas e com relatório, como o Genius."""
        keys = [
            {
                "name": name,
                "displayName": name,
                "type": "PREDEFINED",
                "status": "ACTIVE",
                "reportableType": "ON",
            }
            for name in names
        ]
        created = self._call(
            network_code, "CustomTargetingService", "createCustomTargetingKeys", keys
        )
        self._log_write(network_code, "custom_keys", len(created))
        return {str(key["name"]): str(key["id"]) for key in created}

    def create_key_values(self, network_code: str, key_id: str, values: list[str]) -> int:
        """ESCREVE: cria os valores EXACT que faltam na key, em lotes de 500."""
        statement = self._statement("customTargetingKeyId = :key", {"key": int(key_id)})
        known = {
            str(value["name"])
            for value in self._all(
                network_code,
                "CustomTargetingService",
                "getCustomTargetingValuesByStatement",
                statement,
            )
        }
        missing = [value for value in values if value not in known]
        for start in range(0, len(missing), CREATE_BATCH):
            batch = [
                {
                    "customTargetingKeyId": int(key_id),
                    "name": value,
                    "displayName": value,
                    "matchType": "EXACT",
                }
                for value in missing[start : start + CREATE_BATCH]
            ]
            self._call(network_code, "CustomTargetingService", "createCustomTargetingValues", batch)
        self._log_write(network_code, "key_values", len(missing))
        return len(missing)

    def ensure_key_values(self, network_code: str, key_id: str, values: list[str]) -> list[str]:
        """ESCREVE: cria os valores sem consultar antes, em lotes de 500; os recusados saem do lote
        (duplicados contam como existentes) e o resto vai de novo. Devolve os que existem."""
        existing: list[str] = []
        for start in range(0, len(values), CREATE_BATCH):
            existing += self._create_values(
                network_code, key_id, values[start : start + CREATE_BATCH]
            )
        self._log_write(network_code, "traffic_key_values", len(existing))
        return existing

    def _create_values(self, network_code: str, key_id: str, batch: list[str]) -> list[str]:
        """Um lote: a cada recusa do GAM, tira os itens recusados e manda o resto."""
        pending, duplicated = list(batch), []
        while pending:
            payload = [
                {
                    "customTargetingKeyId": int(key_id),
                    "name": value,
                    "displayName": value,
                    "matchType": "EXACT",
                }
                for value in pending
            ]
            try:
                self._call(
                    network_code, "CustomTargetingService", "createCustomTargetingValues", payload
                )
            except GamError as error:
                refused = _refused_values(error.__cause__, len(pending))
                if not refused:
                    raise
                for index, reason in refused.items():
                    if reason == DUPLICATE:
                        duplicated.append(pending[index])
                    else:
                        log.warning("valor recusado pelo GAM", extra={"reason": reason})
                pending = [value for index, value in enumerate(pending) if index not in refused]
                continue
            return duplicated + pending
        return duplicated

    def find_order(self, network_code: str, name: str) -> GamOrderRef | None:
        """A order com esse nome (só leitura)."""
        statement = self._statement("name = :name", {"name": name}, limit=1)
        order = self._first(network_code, "OrderService", "getOrdersByStatement", statement)
        return _order_ref(order) if order is not None else None

    def create_order(self, network_code: str, name: str) -> GamOrderRef:
        """ESCREVE: cria a order com o anunciante "google" (e o anunciante, se faltar)."""
        advertiser_id = self._advertiser_id(network_code)
        trafficker = self._first(
            network_code,
            "UserService",
            "getUsersByStatement",
            self._statement("status = :status", {"status": "ACTIVE"}, limit=1),
        )
        if trafficker is None:
            raise GamError(f"{network_code}: nenhum usuário ativo para ser o trafficker")
        order = {"name": name, "advertiserId": advertiser_id, "traffickerId": trafficker["id"]}
        created = self._call(network_code, "OrderService", "createOrders", [order])
        self._log_write(network_code, "order", 1)
        return _order_ref(created[0])

    def find_parent_ad_unit(self, network_code: str, domain: str) -> str | None:
        """O bloco ativo com o nome do domínio (só leitura)."""
        statement = self._statement(
            "name = :name AND status = :status", {"name": domain, "status": "ACTIVE"}, limit=1
        )
        unit = self._first(network_code, "InventoryService", "getAdUnitsByStatement", statement)
        return str(unit["id"]) if unit is not None else None

    def create_parent_ad_unit(self, network_code: str, domain: str, root_id: str) -> str:
        """ESCREVE: cria o bloco pai do domínio abaixo do bloco raiz."""
        unit = {"name": domain, "adUnitCode": domain, "parentId": root_id}
        created = self._call(network_code, "InventoryService", "createAdUnits", [unit])
        self._log_write(network_code, "parent_ad_unit", 1)
        return str(created[0]["id"])

    def child_ad_units(self, network_code: str, parent_id: str) -> dict[str, str]:
        """Os blocos filhos ativos do bloco pai (só leitura)."""
        statement = self._statement(
            "parentId = :parent AND status = :status", {"parent": parent_id, "status": "ACTIVE"}
        )
        return {
            str(unit["name"]): str(unit["id"])
            for unit in self._all(
                network_code, "InventoryService", "getAdUnitsByStatement", statement
            )
        }

    def create_child_ad_units(
        self, network_code: str, parent_id: str, blocks: list[BlockSpec]
    ) -> dict[str, str]:
        """ESCREVE: cria os blocos filhos, com os tamanhos e as opções de cada tipo."""
        units = [_ad_unit(parent_id, block) for block in blocks]
        created = self._call(network_code, "InventoryService", "createAdUnits", units)
        self._log_write(network_code, "child_ad_units", len(created))
        return {str(unit["name"]): str(unit["id"]) for unit in created}

    def line_items(self, network_code: str, names: list[str]) -> dict[str, str]:
        """Os line items com esses nomes (só leitura)."""
        statement = self._statement("name IN (:names)", {"names": names})
        return {
            str(item["name"]): str(item["id"])
            for item in self._all(
                network_code, "LineItemService", "getLineItemsByStatement", statement
            )
        }

    def create_line_items(
        self, network_code: str, order_id: str, items: list[LineItemSpec]
    ) -> dict[str, str]:
        """ESCREVE: cria os line items Ad Exchange (CPM zero, sem fim, criativo 0x0)."""
        payload = [_line_item(order_id, item) for item in items]
        created = self._call(network_code, "LineItemService", "createLineItems", payload)
        self._log_write(network_code, "line_items", len(created))
        return {str(item["name"]): str(item["id"]) for item in created}

    def add_line_item_targets(
        self, network_code: str, line_item_id: str, ad_unit_ids: list[str]
    ) -> int:
        """ESCREVE: junta os blocos novos aos que o line item já mira (updateLineItems)."""
        statement = self._statement("id = :id", {"id": int(line_item_id)}, limit=1)
        item = self._first(network_code, "LineItemService", "getLineItemsByStatement", statement)
        if item is None:
            raise GamError(f"{network_code}: line item {line_item_id} não existe")
        inventory = item["targeting"]["inventoryTargeting"]
        targeted = list(inventory["targetedAdUnits"] or [])
        known = {str(target["adUnitId"]) for target in targeted}
        new = [unit_id for unit_id in dict.fromkeys(ad_unit_ids) if unit_id not in known]
        if not new:
            return 0
        targeted += [{"adUnitId": unit_id, "includeDescendants": True} for unit_id in new]
        inventory["targetedAdUnits"] = targeted
        self._call(network_code, "LineItemService", "updateLineItems", [item])
        self._log_write(network_code, "line_item_targets", len(new))
        return len(new)

    def find_creative(self, network_code: str, advertiser_id: str) -> str | None:
        """O criativo Ad Exchange "todos os tamanhos pedidos" do anunciante (só leitura)."""
        statement = self._statement(
            "advertiserId = :advertiser", {"advertiser": int(advertiser_id)}
        )
        for creative in self._all(
            network_code, "CreativeService", "getCreativesByStatement", statement
        ):
            if (
                type(creative).__name__ == "AdExchangeCreative"
                and creative["isAllowsAllRequestedSizes"]
            ):
                return str(creative["id"])
        return None

    def create_creative(self, network_code: str, advertiser_id: str) -> str:
        """ESCREVE: cria o criativo Ad Exchange 1x1 que aceita todos os tamanhos pedidos."""
        creative = {
            "xsi_type": "AdExchangeCreative",
            "name": CREATIVE_NAME.format(moment=datetime.now(UTC).strftime("%Y-%m-%d, %H:%M:%S")),
            "advertiserId": int(advertiser_id),
            "size": {"width": 1, "height": 1, "isAspectRatio": False},
            "isAllowsAllRequestedSizes": True,
            "codeSnippet": CREATIVE_SNIPPET,
        }
        created = self._call(network_code, "CreativeService", "createCreatives", [creative])
        self._log_write(network_code, "creative", 1)
        return str(created[0]["id"])

    def associate_creative(
        self, network_code: str, creative_id: str, line_item_ids: list[str]
    ) -> int:
        """ESCREVE: liga o criativo aos line items que ainda não têm a ligação."""
        ids = [int(item_id) for item_id in dict.fromkeys(line_item_ids)]
        statement = self._statement(
            "creativeId = :creative AND lineItemId IN (:items)",
            {"creative": int(creative_id), "items": ids},
        )
        known = {
            int(association["lineItemId"])
            for association in self._all(
                network_code,
                "LineItemCreativeAssociationService",
                "getLineItemCreativeAssociationsByStatement",
                statement,
            )
        }
        missing = [
            {"creativeId": int(creative_id), "lineItemId": item_id}
            for item_id in ids
            if item_id not in known
        ]
        if missing:
            self._call(
                network_code,
                "LineItemCreativeAssociationService",
                "createLineItemCreativeAssociations",
                missing,
            )
            self._log_write(network_code, "creative_associations", len(missing))
        return len(missing)

    def approve_order(self, network_code: str, order_id: str) -> bool:
        """ESCREVE: aprova a order (ApproveOrders); falso se ela já estava aprovada."""
        statement = self._statement("id = :id", {"id": int(order_id)}, limit=1)
        order = self._first(network_code, "OrderService", "getOrdersByStatement", statement)
        if order is None:
            raise GamError(f"{network_code}: order {order_id} não existe")
        if order["status"] == "APPROVED":
            return False
        self._call(
            network_code,
            "OrderService",
            "performOrderAction",
            {"xsi_type": "ApproveOrders"},
            statement,
        )
        self._log_write(network_code, "approve_order", 1)
        return True

    def _advertiser_id(self, network_code: str) -> int:
        """O anunciante "google"; ESCREVE quando ele não existe e precisa ser criado."""
        statement = self._statement(
            "name = :name AND type = :type",
            {"name": ADVERTISER_NAME, "type": "ADVERTISER"},
            limit=1,
        )
        found = self._first(network_code, "CompanyService", "getCompaniesByStatement", statement)
        if found is not None:
            return int(found["id"])
        company = {"name": ADVERTISER_NAME, "type": "ADVERTISER"}
        created = self._call(network_code, "CompanyService", "createCompanies", [company])
        self._log_write(network_code, "advertiser", 1)
        return int(created[0]["id"])

    def _statement(self, where: str, values: dict[str, Any], *, limit: int | None = None) -> Any:
        """Um StatementBuilder com o filtro e as variáveis."""
        builder = ad_manager.StatementBuilder(version=self._version)
        builder.Where(where)
        for name, value in values.items():
            builder.WithBindVariable(name, value)
        if limit is not None:
            builder.limit = limit
        return builder

    def _first(self, network_code: str, service: str, method: str, builder: Any) -> Any:
        """O primeiro resultado da consulta, ou ``None``."""
        response = self._call(network_code, service, method, builder.ToStatement())
        results = response["results"] if response is not None else None
        return results[0] if results else None

    def _all(self, network_code: str, service: str, method: str, builder: Any) -> Iterator[Any]:
        """Todos os resultados da consulta, página a página."""
        while True:
            response = self._call(network_code, service, method, builder.ToStatement())
            results = response["results"] if response is not None else None
            if not results:
                return
            yield from results
            builder.offset += builder.limit

    def _call(self, network_code: str, service: str, method: str, *args: Any) -> Any:
        """Chama o método do serviço SOAP, convertendo as falhas em erros do avant-core."""
        try:
            soap = self._client(network_code).GetService(service, version=self._version)
            return getattr(soap, method)(*args)
        except errors.GoogleAdsServerFault as error:
            raise _classify(network_code, error) from error
        except auth_exceptions.RefreshError as error:
            raise GamAccessDenied(f"a conta de serviço não autenticou: {error}") from error
        except (auth_exceptions.TransportError, OSError) as error:
            raise GamUnavailable(f"falha de rede no GAM: {error}") from error

    def _client(self, network_code: str) -> ad_manager.AdManagerClient:
        """Cliente do googleads da network, reaproveitando o token da conta de serviço."""
        if self._oauth is None:
            self._oauth = oauth2.GoogleServiceAccountClient(
                self._key_file, oauth2.GetAPIScope("ad_manager")
            )
        if network_code not in self._clients:
            self._clients[network_code] = ad_manager.AdManagerClient(
                self._oauth, APPLICATION_NAME, network_code=network_code
            )
        return self._clients[network_code]

    def _log_write(self, network_code: str, what: str, count: int) -> None:
        """Registra no log cada escrita feita no GAM."""
        log.info(
            "escrita no GAM", extra={"network_code": network_code, "what": what, "count": count}
        )


def _order_ref(order: Any) -> GamOrderRef:
    """A order do SOAP no formato do avant-core."""
    return GamOrderRef(
        gam_id=str(order["id"]),
        advertiser_id=str(order["advertiserId"]),
        approved=order["status"] == "APPROVED",
    )


def _ad_unit(parent_id: str, block: BlockSpec) -> dict[str, Any]:
    """O bloco filho como o Genius cria: código igual ao nome, janela TOP, tamanhos BROWSER."""
    unit: dict[str, Any] = {
        "name": block.name,
        "adUnitCode": block.name,
        "parentId": parent_id,
        "targetWindow": "TOP",
        "adUnitSizes": [
            {
                "size": {"width": width, "height": height, "isAspectRatio": False},
                "environmentType": "BROWSER",
            }
            for width, height in block.sizes
        ],
    }
    if block.interstitial:
        unit["isInterstitial"] = True
    if block.fluid:
        unit["isFluid"] = True
    return unit


def _line_item(order_id: str, item: LineItemSpec) -> dict[str, Any]:
    """O line item Ad Exchange como o Genius cria."""
    return {
        "orderId": int(order_id),
        "name": item.name,
        "lineItemType": "AD_EXCHANGE",
        "environmentType": "BROWSER",
        "startDateTimeType": "IMMEDIATELY",
        "unlimitedEndDateTime": True,
        "costType": "CPM",
        "costPerUnit": {"currencyCode": item.currency_code, "microAmount": 0},
        "primaryGoal": {"goalType": "NONE"},
        "creativePlaceholders": [
            {
                "size": {"width": 0, "height": 0, "isAspectRatio": False},
                "creativeSizeType": "IGNORED",
            }
        ],
        "webPropertyCode": item.web_property_code,
        "targeting": {
            "inventoryTargeting": {
                "targetedAdUnits": [
                    {"adUnitId": unit_id, "includeDescendants": item.include_descendants}
                    for unit_id in item.ad_unit_ids
                ]
            }
        },
    }


def _refused_values(fault: BaseException | None, size: int) -> dict[int, str]:
    """Os itens do lote que o GAM recusou (índice para o motivo); vazio quando a falha não aponta
    item nenhum (cota, rede), para quem chama deixar o erro subir."""
    if not isinstance(fault, errors.GoogleAdsServerFault):
        return {}
    refused: dict[int, str] = {}
    for error in fault.errors or []:
        found = re.search(r"\[(\d+)\]", str(getattr(error, "fieldPath", "") or ""))
        if found is None or int(found.group(1)) >= size:
            return {}
        refused[int(found.group(1))] = str(getattr(error, "reason", "") or "")
    return refused
