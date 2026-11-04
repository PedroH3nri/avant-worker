"""Busca as páginas dos sites dos clientes para o checklist de domínio.

É a primeira vez que o worker acessa os sites dos clientes: só GET, sem executar
JavaScript, com o User-Agent do Avant, tempo curto, no máximo 2 MB por página e um pedido
por segundo em cada domínio.

O domínio vem do GAM do cliente, que controla o nome e o DNS: toda conexão (inclusive a de um
redirecionamento) passa pelo ``PublicOnlyBackend``, que resolve o host, recusa endereço privado,
loopback, link-local ou reservado e portas fora de 80 e 443, e conecta no IP já conferido, sem
resolver de novo (contra DNS rebinding).
"""

import ipaddress
import socket
import time
from collections.abc import Iterable
from urllib.parse import urlparse

import httpcore
import httpx
from avant_core.site_checklists.models import FetchedPage

USER_AGENT = "AvantChecklist/1.0 (+https://avant.groone.com)"
TIMEOUT_SECONDS = 10.0
MAX_BYTES = 2 * 1024 * 1024
DOMAIN_INTERVAL_SECONDS = 1.0
TOTAL_SECONDS = 20.0
ALLOWED_PORTS = frozenset({80, 443})


def public_address(address: str) -> bool:
    """Diz se o IP é da internet pública (nem privado, loopback, link-local ou reservado)."""
    ip = ipaddress.ip_address(address)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


class PublicOnlyBackend(httpcore.SyncBackend):
    """Conecta só em IP público nas portas 80 e 443, no endereço que acabou de conferir."""

    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options: Iterable[httpcore.SOCKET_OPTION] | None = None,
    ) -> httpcore.NetworkStream:
        """Resolve o host, recusa se algum endereço não for público e conecta no primeiro."""
        if port not in ALLOWED_PORTS:
            raise httpcore.ConnectError(f"porta {port} recusada")
        try:
            found = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        except OSError as exc:
            raise httpcore.ConnectError(f"{host} não resolveu") from exc
        addresses = [str(item[4][0]) for item in found]
        if not addresses or not all(public_address(address) for address in addresses):
            raise httpcore.ConnectError(f"{host} aponta para um endereço interno")
        return super().connect_tcp(addresses[0], port, timeout, local_address, socket_options)


def _public_transport() -> httpx.HTTPTransport:
    """O transporte do httpx com a conexão passando pelo ``PublicOnlyBackend``."""
    transport = httpx.HTTPTransport()
    transport._pool._network_backend = PublicOnlyBackend()
    return transport


class HttpPageFetcher:
    """Cliente HTTP do checklist: segue redirecionamentos e lê só texto."""

    def __init__(self, http: httpx.Client | None = None, interval: float = DOMAIN_INTERVAL_SECONDS):
        self._http = http or httpx.Client(
            transport=_public_transport(),
            timeout=TIMEOUT_SECONDS,
            follow_redirects=True,
            max_redirects=5,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,text/plain;q=0.9"},
        )
        self._interval = interval
        self._last_request: dict[str, float] = {}

    def fetch(self, url: str) -> FetchedPage | None:
        """A página com o endereço final e o código; ``None`` quando o site não responde."""
        self._wait_for(urlparse(url).hostname or "")
        try:
            with self._http.stream("GET", url) as response:
                body = self._read(response)
                return FetchedPage(str(response.url), response.status_code, body)
        except httpx.HTTPError:
            return None

    def _wait_for(self, host: str) -> None:
        """Espera o intervalo mínimo desde o último pedido ao mesmo domínio."""
        last = self._last_request.get(host)
        if last is not None:
            pause = self._interval - (time.monotonic() - last)
            if pause > 0:
                time.sleep(pause)
        self._last_request[host] = time.monotonic()

    def _read(self, response: httpx.Response) -> str:
        """O texto da resposta até 2 MB e 20 segundos; o que não é texto volta vazio."""
        kind = response.headers.get("content-type", "text/html").lower()
        if "html" not in kind and "text" not in kind:
            return ""
        deadline = time.monotonic() + TOTAL_SECONDS
        chunks: list[bytes] = []
        size = 0
        for chunk in response.iter_bytes():
            chunks.append(chunk)
            size += len(chunk)
            if size >= MAX_BYTES or time.monotonic() > deadline:
                break
        return b"".join(chunks)[:MAX_BYTES].decode(response.encoding or "utf-8", errors="replace")
