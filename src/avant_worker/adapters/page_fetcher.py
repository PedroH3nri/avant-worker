"""Busca as páginas dos sites dos clientes para o checklist de domínio.

É a primeira vez que o worker acessa os sites dos clientes: só GET, sem executar
JavaScript, com o User-Agent do Avant, tempo curto, no máximo 2 MB por página e um pedido
por segundo em cada domínio.

O domínio vem do GAM do cliente, que controla o nome e o DNS: toda conexão (inclusive a de um
redirecionamento) passa pelo ``PublicOnlyBackend``, que resolve o host, recusa endereço privado,
loopback, link-local ou reservado e portas fora de 80 e 443, e conecta no IP já conferido, sem
resolver de novo (contra DNS rebinding). Endereço IPv6 que carrega um IPv4 (mapeado, compatível,
SIIT ``::ffff:0:0:0/96``, NAT64 ``64:ff9b::/96``, 6to4 e Teredo) vale pelo IPv4 de dentro; o
NAT64 local ``64:ff9b:1::/48`` é sempre recusado. Os endereços conferidos são tentados em ordem.

Um NAT64 com prefixo próprio da rede (fora dos prefixos conhecidos) não se reconhece pelo
endereço: a defesa definitiva contra SSRF é o firewall de saída da VM (avant-infra).

Cada busca tem um prazo total de 20 segundos que cobre o DNS, a conexão, o TLS, os cabeçalhos,
os redirecionamentos e o corpo: toda leitura e escrita na rede usa só o tempo que sobra.
Se o prazo acaba no meio do corpo, a página volta com o que chegou até ali (truncada, sem
marca): o checklist confere o que está no começo da página e o ads.txt é pequeno.
"""

import contextlib
import ipaddress
import socket
import ssl
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as LookupTimeout
from contextvars import ContextVar
from typing import Any
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
RESOLVER_THREADS = 8
IPV4_COMPATIBLE = ipaddress.IPv6Network("::/96")
IPV4_TRANSLATED_SIIT = ipaddress.IPv6Network("::ffff:0:0:0/96")
NAT64_WELL_KNOWN = ipaddress.IPv6Network("64:ff9b::/96")
NAT64_LOCAL = ipaddress.IPv6Network("64:ff9b:1::/48")
IPV4_BITS = 0xFFFFFFFF

_deadline: ContextVar[float | None] = ContextVar("avant_fetch_deadline", default=None)
_resolver = ThreadPoolExecutor(max_workers=RESOLVER_THREADS, thread_name_prefix="avant-dns")


def public_address(address: str) -> bool:
    """Diz se o IP é da internet pública (nem privado, loopback, link-local ou reservado).
    No IPv6 que leva um IPv4 dentro, quem decide é o IPv4; o NAT64 local é sempre recusado."""
    ip = ipaddress.ip_address(address)
    if isinstance(ip, ipaddress.IPv4Address):
        return _public_ipv4(ip)
    if ip in NAT64_LOCAL:
        return False
    embedded = _embedded_ipv4(ip)
    if embedded:
        return all(_public_ipv4(inner) for inner in embedded)
    return ip.is_global and not ip.is_multicast


def _public_ipv4(ip: ipaddress.IPv4Address) -> bool:
    """Diz se o IPv4 é da internet pública."""
    return ip.is_global and not ip.is_multicast


def _embedded_ipv4(ip: ipaddress.IPv6Address) -> list[ipaddress.IPv4Address]:
    """Os IPv4 que o endereço IPv6 alcança: mapeado, compatível, SIIT, NAT64, 6to4 ou Teredo."""
    if ip.ipv4_mapped is not None:
        return [ip.ipv4_mapped]
    if ip in IPV4_COMPATIBLE or ip in IPV4_TRANSLATED_SIIT or ip in NAT64_WELL_KNOWN:
        return [ipaddress.IPv4Address(int(ip) & IPV4_BITS)]
    if ip.sixtofour is not None:
        return [ip.sixtofour]
    if ip.teredo is not None:
        return list(ip.teredo)
    return []


def _time_left(timeout: float | None, error: type[Exception]) -> float | None:
    """O tempo da operação limitado ao que sobra do prazo da busca; esgotado, levanta ``error``."""
    deadline = _deadline.get()
    if deadline is None:
        return timeout
    left = deadline - time.monotonic()
    if left <= 0:
        raise error("prazo total da busca esgotado")
    return left if timeout is None else min(timeout, left)


def _resolve(host: str, port: int, timeout: float | None) -> list[str]:
    """Os endereços do host, sem repetir, com o DNS dentro do prazo da busca.
    No tempo esgotado, cancela a consulta que ainda espera na fila do pool."""
    wait = _time_left(timeout, httpcore.ConnectTimeout)
    lookup = _resolver.submit(socket.getaddrinfo, host, port, type=socket.SOCK_STREAM)
    try:
        found = lookup.result(timeout=wait)
    except LookupTimeout as exc:
        lookup.cancel()
        raise httpcore.ConnectTimeout(f"{host} não resolveu a tempo") from exc
    except OSError as exc:
        raise httpcore.ConnectError(f"{host} não resolveu") from exc
    return list(dict.fromkeys(str(item[4][0]) for item in found))


class DeadlineStream(httpcore.NetworkStream):
    """Conexão em que cada leitura, escrita e TLS usa só o que sobra do prazo da busca."""

    def __init__(self, stream: httpcore.NetworkStream) -> None:
        self._stream = stream

    def read(self, max_bytes: int, timeout: float | None = None) -> bytes:
        """Lê da conexão dentro do prazo."""
        return self._stream.read(max_bytes, _time_left(timeout, httpcore.ReadTimeout))

    def write(self, buffer: bytes, timeout: float | None = None) -> None:
        """Escreve na conexão dentro do prazo."""
        self._stream.write(buffer, _time_left(timeout, httpcore.WriteTimeout))

    def close(self) -> None:
        """Fecha a conexão."""
        self._stream.close()

    def start_tls(
        self,
        ssl_context: ssl.SSLContext,
        server_hostname: str | None = None,
        timeout: float | None = None,
    ) -> httpcore.NetworkStream:
        """Abre o TLS dentro do prazo e continua limitando a conexão cifrada."""
        tls_timeout = _time_left(timeout, httpcore.ConnectTimeout)
        return DeadlineStream(self._stream.start_tls(ssl_context, server_hostname, tls_timeout))

    def get_extra_info(self, info: str) -> Any:
        """Repassa as informações da conexão de baixo."""
        return self._stream.get_extra_info(info)


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
        """Resolve o host, recusa se algum endereço não for público e tenta cada um, em ordem."""
        if port not in ALLOWED_PORTS:
            raise httpcore.ConnectError(f"porta {port} recusada")
        addresses = _resolve(host, port, timeout)
        if not addresses or not all(public_address(address) for address in addresses):
            raise httpcore.ConnectError(f"{host} aponta para um endereço interno")
        options = list(socket_options or [])
        failure: httpcore.ConnectError | httpcore.ConnectTimeout | None = None
        for address in addresses:
            connect_timeout = _time_left(timeout, httpcore.ConnectTimeout)
            try:
                stream = super().connect_tcp(address, port, connect_timeout, local_address, options)
            except (httpcore.ConnectError, httpcore.ConnectTimeout) as exc:
                failure = exc
                continue
            return DeadlineStream(stream)
        if failure is None:
            raise httpcore.ConnectError(f"{host} sem endereço para conectar")
        raise failure


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
        token = _deadline.set(time.monotonic() + TOTAL_SECONDS)
        try:
            with self._http.stream("GET", url) as response:
                body = self._read(response)
                return FetchedPage(str(response.url), response.status_code, body)
        except httpx.HTTPError:
            return None
        finally:
            _deadline.reset(token)

    def _wait_for(self, host: str) -> None:
        """Espera o intervalo mínimo desde o último pedido ao mesmo domínio."""
        last = self._last_request.get(host)
        if last is not None:
            pause = self._interval - (time.monotonic() - last)
            if pause > 0:
                time.sleep(pause)
        self._last_request[host] = time.monotonic()

    def _read(self, response: httpx.Response) -> str:
        """O texto da resposta até 2 MB ou o fim do prazo (o que chegou, sem marca de corte).
        O que não é texto volta vazio."""
        kind = response.headers.get("content-type", "text/html").lower()
        if "html" not in kind and "text" not in kind:
            return ""
        chunks: list[bytes] = []
        size = 0
        with contextlib.suppress(httpx.TimeoutException):
            for chunk in response.iter_bytes():
                chunks.append(chunk)
                size += len(chunk)
                if size >= MAX_BYTES:
                    break
        return b"".join(chunks)[:MAX_BYTES].decode(response.encoding or "utf-8", errors="replace")
