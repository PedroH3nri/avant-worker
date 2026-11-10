"""O país pelo IP com a base GeoLite2 Country da MaxMind (arquivo .mmdb no disco do worker).

A base é baixada fora do worker (conta da MaxMind, atualização semanal) e montada no container;
o caminho vem de ``GEOLITE2_COUNTRY_FILE``. O IP só passa por aqui e não é gravado.
"""

import ipaddress
from typing import Any

import maxminddb


class GeoLiteCountries:
    """Busca o nome do país em inglês, como o data guardava (``Brazil``)."""

    def __init__(self, path: str) -> None:
        self._reader = maxminddb.open_database(path)

    def country(self, ip: str | None) -> str | None:
        """O país do IP, ou vazio quando o IP não vale ou não está na base."""
        if not ip:
            return None
        try:
            ipaddress.ip_address(ip)
            found: Any = self._reader.get(ip)
        except ValueError:
            return None
        if not isinstance(found, dict):
            return None
        names = (found.get("country") or found.get("registered_country") or {}).get("names", {})
        return names.get("en") if isinstance(names, dict) else None
