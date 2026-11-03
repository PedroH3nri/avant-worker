"""Busca as páginas dos sites dos clientes para o checklist de domínio.

É a primeira vez que o worker acessa os sites dos clientes: só GET, sem executar
JavaScript, com o User-Agent do Avant, tempo curto, no máximo 2 MB por página e um pedido
por segundo em cada domínio.
"""

import time
from urllib.parse import urlparse

import httpx
from avant_core.site_checklists.models import FetchedPage

USER_AGENT = "AvantChecklist/1.0 (+https://avant.groone.com)"
TIMEOUT_SECONDS = 10.0
MAX_BYTES = 2 * 1024 * 1024
DOMAIN_INTERVAL_SECONDS = 1.0


class HttpPageFetcher:
    """Cliente HTTP do checklist: segue redirecionamentos e lê só texto."""

    def __init__(self, http: httpx.Client | None = None, interval: float = DOMAIN_INTERVAL_SECONDS):
        self._http = http or httpx.Client(
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
        """O texto da resposta até 2 MB; o que não é texto volta vazio."""
        kind = response.headers.get("content-type", "text/html").lower()
        if "html" not in kind and "text" not in kind:
            return ""
        chunks: list[bytes] = []
        size = 0
        for chunk in response.iter_bytes():
            chunks.append(chunk)
            size += len(chunk)
            if size >= MAX_BYTES:
                break
        return b"".join(chunks)[:MAX_BYTES].decode(response.encoding or "utf-8", errors="replace")
