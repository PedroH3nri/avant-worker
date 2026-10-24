"""Adaptador do GamClient do avant-core para a API REST do Google Ad Manager (v1).

Só leitura: o escopo é ``admanager.readonly`` e nenhum método escreve no GAM. A conta de
serviço da Groone entra pelo arquivo de chave JSON (``GAM_SERVICE_ACCOUNT_FILE``), que
existe só nas VMs dos workers da fila ``gam``.

Erros saem já classificados para o avant-core:

- 401 e 403: ``GamAccessDenied`` (API desligada ou conta de serviço sem acesso);
- 404: ``GamNetworkNotFound``;
- 429, 5xx, timeout e falha de rede: ``GamUnavailable`` (temporário, a tarefa tenta de novo);
- outro 4xx: ``GamError`` permanente.
"""

import logging
import time
from collections.abc import Iterator, Mapping
from typing import Any

import httpx
from avant_core.gam.domain import Delegation, InventoryStatus
from avant_core.ports import (
    GamAccessDenied,
    GamAdUnit,
    GamChildPublisher,
    GamError,
    GamNetworkInfo,
    GamNetworkNotFound,
    GamSite,
    GamUnavailable,
)
from google.auth import exceptions as auth_exceptions
from google.auth.credentials import Credentials
from google.auth.transport import Request as AuthRequest
from google.auth.transport import Response as AuthResponse
from google.oauth2 import service_account

BASE_URL = "https://admanager.googleapis.com/v1/"
SCOPES = ("https://www.googleapis.com/auth/admanager.readonly",)
PAGE_SIZE = 1000
# Papel predefinido "Administrador" do Ad Manager (os papéis do Google têm id negativo).
ADMINISTRATOR_ROLE_ID = "-1"

log = logging.getLogger("avant.worker.gam")


class RestGamClient:
    def __init__(
        self,
        credentials: Credentials,
        *,
        service_account_email: str,
        http: httpx.Client | None = None,
    ) -> None:
        self._credentials = credentials
        self._email = service_account_email
        self._http = http or httpx.Client(base_url=BASE_URL, timeout=30.0)
        self._auth_request = _HttpxAuthRequest(self._http)

    @classmethod
    def from_key_file(cls, path: str) -> "RestGamClient":
        """Monta o cliente a partir do arquivo de chave da conta de serviço."""
        credentials = service_account.Credentials.from_service_account_file(  # type: ignore[no-untyped-call]
            path, scopes=SCOPES
        )
        return cls(credentials, service_account_email=credentials.service_account_email)

    @property
    def service_account_email(self) -> str:
        """Devolve o email da conta de serviço."""
        return self._email

    # --- GamClient ---------------------------------------------------------------------

    def get_network(self, network_code: str) -> GamNetworkInfo:
        """Lê o nome da network e se ela é de teste."""
        data = self._get(f"networks/{network_code}")
        return GamNetworkInfo(
            network_code=str(data.get("networkCode") or network_code),
            display_name=str(data.get("displayName") or ""),
            is_test=bool(data.get("testNetwork", False)),
        )

    def is_admin(self, network_code: str) -> bool:
        """Diz se a conta de serviço é administradora ativa na network."""
        current_user = self._get(f"networks/{network_code}/users/me")
        role = str(current_user.get("role") or "").rsplit("/", 1)[-1]
        return bool(current_user.get("active", True)) and role == ADMINISTRATOR_ROLE_ID

    def list_child_publishers(self, network_code: str) -> Iterator[GamChildPublisher]:
        """Lista as networks filhas do MCM da network."""
        for item in self._list(f"networks/{network_code}/childPublishers", "childPublishers"):
            child_code = _last(item.get("childNetwork"))
            if not child_code:
                continue
            yield GamChildPublisher(
                network_code=child_code,
                display_name=item.get("displayName") or None,
                email=str(item.get("email") or ""),
                delegation=_delegation(item.get("delegationType")),
                account_status=str(item.get("accountStatus") or "UNSPECIFIED"),
            )

    def list_sites(self, network_code: str) -> Iterator[GamSite]:
        """Lista os sites da network."""
        for item in self._list(f"networks/{network_code}/sites", "sites"):
            yield GamSite(
                gam_id=_last(item.get("name")),
                url=str(item.get("url") or ""),
                approval_status=item.get("approvalStatus") or None,
                child_network_code=item.get("childNetworkCode") or None,
            )

    def list_ad_units(self, network_code: str) -> Iterator[GamAdUnit]:
        """Sem a raiz da network; quem fica logo abaixo dela sai com pai vazio. Os
        arquivados no GAM ficam de fora: a importação arquiva o que não veio."""
        items = list(self._list(f"networks/{network_code}/adUnits", "adUnits"))
        roots = {_last(item.get("name")) for item in items if not item.get("parentAdUnit")}
        for item in items:
            gam_id = _last(item.get("name"))
            status = str(item.get("status") or "ACTIVE")
            if gam_id in roots or status == "ARCHIVED":
                continue
            parent = _last(item.get("parentAdUnit"))
            yield GamAdUnit(
                gam_id=gam_id,
                parent_gam_id=None if parent in roots else parent,
                name=str(item.get("displayName") or ""),
                code=item.get("adUnitCode") or None,
                status=InventoryStatus.INACTIVE if status == "INACTIVE" else InventoryStatus.ACTIVE,
            )

    # --- HTTP --------------------------------------------------------------------------

    def _list(self, path: str, key: str) -> Iterator[dict[str, Any]]:
        """Percorre todas as páginas de uma listagem da API REST do GAM."""
        token: str | None = None
        while True:
            params: dict[str, str | int] = {"pageSize": PAGE_SIZE}
            if token:
                params["pageToken"] = token
            page = self._get(path, params)
            yield from page.get(key) or []
            token = page.get("nextPageToken")
            if not token:
                return

    def _get(self, path: str, params: Mapping[str, str | int] | None = None) -> dict[str, Any]:
        """Faz um GET autenticado na API REST do GAM, medindo a duração."""
        started = time.monotonic()
        try:
            self._credentials.before_request(self._auth_request, "GET", path, {})  # type: ignore[no-untyped-call]
            headers: dict[str, str] = {}
            self._credentials.apply(headers)  # type: ignore[no-untyped-call]
            response = self._http.get(path, params=params, headers=headers)
        except httpx.TimeoutException as exc:
            raise GamUnavailable(f"tempo esgotado em {path}") from exc
        except httpx.TransportError as exc:
            raise GamUnavailable(f"falha de rede em {path}: {exc}") from exc
        except auth_exceptions.TransportError as exc:
            raise GamUnavailable(f"falha ao renovar o token: {exc}") from exc
        except auth_exceptions.RefreshError as exc:
            raise GamAccessDenied(f"a conta de serviço não autenticou: {exc}") from exc
        elapsed = round((time.monotonic() - started) * 1000)
        if response.status_code >= 400:
            log.warning(
                "GAM respondeu erro",
                extra={"path": path, "status": response.status_code, "ms": elapsed},
            )
            raise _error(path, response)
        log.debug("GAM", extra={"path": path, "status": response.status_code, "ms": elapsed})
        data = response.json()
        return data if isinstance(data, dict) else {}


def _error(path: str, response: httpx.Response) -> GamError:
    """Converte a resposta de erro do GAM em GamError, permanente ou não."""
    status = response.status_code
    message = _message(response) or f"HTTP {status}"
    text = f"{path}: {message}"
    if status in (401, 403):
        return GamAccessDenied(text)
    if status == 404:
        return GamNetworkNotFound(text)
    if status == 429 or status >= 500:
        return GamUnavailable(text)
    return GamError(text)


def _message(response: httpx.Response) -> str | None:
    """Lê a mensagem de erro do corpo da resposta do GAM, se houver."""
    try:
        body = response.json()
    except ValueError:
        return None
    error = body.get("error") if isinstance(body, dict) else None
    return str(error.get("message")) if isinstance(error, dict) and error.get("message") else None


def _last(resource_name: object) -> str:
    """``networks/123/adUnits/456`` → ``456``."""
    return str(resource_name or "").rsplit("/", 1)[-1]


def _delegation(value: object) -> Delegation | None:
    """Converte o tipo de delegação do MCM, se for conhecido."""
    return {
        "MANAGE_ACCOUNT": Delegation.MANAGE_ACCOUNT,
        "MANAGE_INVENTORY": Delegation.MANAGE_INVENTORY,
    }.get(str(value or ""))


class _HttpxResponse(AuthResponse):
    def __init__(self, response: httpx.Response) -> None:
        self._response = response

    @property
    def status(self) -> int:
        """Devolve o status HTTP da resposta."""
        return self._response.status_code

    @property
    def headers(self) -> Mapping[str, str]:
        """Devolve os cabeçalhos da resposta."""
        return self._response.headers

    @property
    def data(self) -> bytes:
        """Devolve o corpo da resposta em bytes."""
        return self._response.content


class _HttpxAuthRequest(AuthRequest):
    """Transporte do google-auth sobre o httpx, para renovar o token da conta de serviço
    sem trazer a biblioteca requests."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def __call__(
        self,
        url: str,
        method: str = "GET",
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> AuthResponse:
        response = self._http.request(
            method, url, content=body, headers=dict(headers or {}), timeout=timeout or 30.0
        )
        return _HttpxResponse(response)
