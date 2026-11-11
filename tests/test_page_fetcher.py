"""Proteção contra SSRF e prazo total do ``HttpPageFetcher`` (worker#92)."""

import socket
import threading
import time
from collections.abc import Callable, Iterator
from typing import Any

import httpcore
import pytest

from avant_worker.adapters import HttpPageFetcher, page_fetcher
from avant_worker.adapters.page_fetcher import PublicOnlyBackend, public_address

TEREDO_PRIVATE_CLIENT = "2001:0:4136:e378:8000:63bf:3fff:fdd2"
TEREDO_PUBLIC_CLIENT = "2001:0:4136:e378:8000:63bf:a247:2bdd"
DRIP_SECONDS = 0.05
SHORT_DEADLINE = 0.6


@pytest.mark.parametrize(
    "address",
    [
        "64:ff9b::a00:5",
        "64:ff9b::7f00:1",
        "64:ff9b:1::5db8:d822",
        "64:ff9b:1::a00:5",
        "::a00:5",
        "::7f00:1",
        "::ffff:a00:5",
        "::ffff:a9fe:a9fe",
        "2002:a00:5::1",
        "2002:a9fe:a9fe::1",
        TEREDO_PRIVATE_CLIENT,
    ],
)
def test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused(address: str) -> None:
    assert not public_address(address)


@pytest.mark.parametrize(
    "address",
    [
        "64:ff9b::5db8:d822",
        "::5db8:d822",
        "::ffff:5db8:d822",
        "2002:5db8:d822::1",
        TEREDO_PUBLIC_CLIENT,
    ],
)
def test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(address: str) -> None:
    assert public_address(address)


def _resolves_to(monkeypatch: pytest.MonkeyPatch, addresses: list[str]) -> None:
    """Faz o DNS devolver os endereços dados, na ordem."""

    def fake_getaddrinfo(host: str, port: int, **_: Any) -> list[Any]:
        """Os endereços cadastrados no formato do ``getaddrinfo``."""
        return [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, port)) for address in addresses
        ]

    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)


class FakeStream(httpcore.NetworkStream):
    """Conexão de mentira que só guarda o endereço em que conectou."""

    def __init__(self, address: str) -> None:
        self.address = address


def test_backend_tries_each_checked_address_in_order(monkeypatch: pytest.MonkeyPatch) -> None:
    _resolves_to(monkeypatch, ["2606:2800:220:1::1", "93.184.216.34", "93.184.216.35"])
    tried: list[str] = []

    def fake_connect(_: Any, host: str, port: int, *args: Any, **kwargs: Any) -> FakeStream:
        """Falha no IPv6 (sem rota) e conecta no primeiro IPv4."""
        tried.append(host)
        if ":" in host:
            raise httpcore.ConnectError("sem rota IPv6")
        return FakeStream(host)

    monkeypatch.setattr(httpcore.SyncBackend, "connect_tcp", fake_connect)
    PublicOnlyBackend().connect_tcp("example.com", 443, timeout=1)
    assert tried == ["2606:2800:220:1::1", "93.184.216.34"]


def test_backend_raises_the_last_error_when_no_address_answers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _resolves_to(monkeypatch, ["93.184.216.34", "93.184.216.35"])
    tried: list[str] = []

    def fake_connect(_: Any, host: str, port: int, *args: Any, **kwargs: Any) -> FakeStream:
        """Nenhum endereço responde."""
        tried.append(host)
        raise httpcore.ConnectError(f"{host} fora do ar")

    monkeypatch.setattr(httpcore.SyncBackend, "connect_tcp", fake_connect)
    with pytest.raises(httpcore.ConnectError, match=r"93\.184\.216\.35"):
        PublicOnlyBackend().connect_tcp("example.com", 443, timeout=1)
    assert tried == ["93.184.216.34", "93.184.216.35"]


def test_backend_never_connects_when_any_address_is_internal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _resolves_to(monkeypatch, ["93.184.216.34", "64:ff9b::a00:5"])
    tried: list[str] = []

    def fake_connect(_: Any, host: str, *args: Any, **kwargs: Any) -> FakeStream:
        """Registra a tentativa, que não deve acontecer."""
        tried.append(host)
        return FakeStream(host)

    monkeypatch.setattr(httpcore.SyncBackend, "connect_tcp", fake_connect)
    with pytest.raises(httpcore.ConnectError):
        PublicOnlyBackend().connect_tcp("example.com", 443, timeout=1)
    assert tried == []


def test_slow_dns_counts_against_the_total_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    def slow_getaddrinfo(*_: Any, **__: Any) -> list[Any]:
        """Um DNS que demora mais que o prazo inteiro."""
        time.sleep(SHORT_DEADLINE * 3)
        return []

    monkeypatch.setattr(socket, "getaddrinfo", slow_getaddrinfo)
    monkeypatch.setattr(page_fetcher, "TOTAL_SECONDS", SHORT_DEADLINE)
    started = time.monotonic()
    assert HttpPageFetcher(interval=0).fetch("http://example.com/") is None
    assert time.monotonic() - started < SHORT_DEADLINE * 2


DrippingServer = Callable[[bytes, bytes], int]


@pytest.fixture
def dripping_server(monkeypatch: pytest.MonkeyPatch) -> Iterator[DrippingServer]:
    """Sobe um servidor local que pinga a resposta; libera o loopback e a porta dele."""
    stop = threading.Event()
    threads: list[threading.Thread] = []

    def start(head: bytes, drip: bytes) -> int:
        """Manda ``head`` de uma vez e repete ``drip`` devagar; devolve a porta."""
        listener = socket.create_server(("127.0.0.1", 0))
        listener.settimeout(5)

        def serve() -> None:
            """Atende uma conexão até o teste acabar."""
            with listener, listener.accept()[0] as connection:
                connection.recv(65536)
                connection.sendall(head)
                while not stop.is_set():
                    try:
                        connection.sendall(drip)
                    except OSError:
                        return
                    time.sleep(DRIP_SECONDS)

        server = threading.Thread(target=serve, daemon=True)
        server.start()
        threads.append(server)
        port: int = listener.getsockname()[1]
        monkeypatch.setattr(page_fetcher, "ALLOWED_PORTS", frozenset({port}))
        return port

    monkeypatch.setattr(page_fetcher, "public_address", lambda _: True)
    monkeypatch.setattr(page_fetcher, "TOTAL_SECONDS", SHORT_DEADLINE)
    yield start
    stop.set()
    for server in threads:
        server.join(timeout=2)


def test_slow_headers_count_against_the_total_deadline(dripping_server: DrippingServer) -> None:
    port = dripping_server(b"HTTP/1.1 200 OK\r\n", b"X-Lento: 1\r\n")
    started = time.monotonic()
    assert HttpPageFetcher(interval=0).fetch(f"http://127.0.0.1:{port}/") is None
    assert time.monotonic() - started < SHORT_DEADLINE * 3


def test_slow_body_stops_at_the_total_deadline_with_what_arrived(
    dripping_server: DrippingServer,
) -> None:
    head = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 1000000\r\n\r\n<p>"
    port = dripping_server(head, b"a")
    started = time.monotonic()
    page = HttpPageFetcher(interval=0).fetch(f"http://127.0.0.1:{port}/")
    assert time.monotonic() - started < SHORT_DEADLINE * 3
    assert page is not None and page.status == 200 and page.body.startswith("<p>a")
