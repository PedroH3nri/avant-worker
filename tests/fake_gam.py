"""Um GAM em memória para as tarefas (o do avant-core fica nos testes dele)."""

from dataclasses import dataclass, field
from datetime import date

from avant_core.metrics.domain import GamReportRow
from avant_core.ports import (
    GamAccessDenied,
    GamAdUnit,
    GamChildPublisher,
    GamError,
    GamNetworkInfo,
    GamSite,
)

from avant_worker.gam_reports import ReportKind


@dataclass
class FakeGamClient:
    service_account_email: str = "avant@groone-ads.iam.gserviceaccount.com"
    networks: dict[str, GamNetworkInfo] = field(default_factory=dict)
    admin_of: set[str] = field(default_factory=set)
    children: list[GamChildPublisher] = field(default_factory=list)
    sites: dict[str, list[GamSite]] = field(default_factory=dict)
    ad_units: dict[str, list[GamAdUnit]] = field(default_factory=dict)
    # Erros que as próximas chamadas a essa network levantam, um por chamada.
    fail_next: dict[str, list[GamError]] = field(default_factory=dict)
    calls: list[tuple[str, str]] = field(default_factory=list)

    def _call(self, method: str, code: str) -> None:
        self.calls.append((method, code))
        if self.fail_next.get(code):
            raise self.fail_next[code].pop(0)

    def get_network(self, network_code: str) -> GamNetworkInfo:
        self._call("get_network", network_code)
        if network_code not in self.networks:
            raise GamAccessDenied(f"sem acesso a {network_code}")
        return self.networks[network_code]

    def is_admin(self, network_code: str) -> bool:
        self._call("is_admin", network_code)
        return network_code in self.admin_of

    def list_child_publishers(self, network_code: str) -> list[GamChildPublisher]:
        self._call("list_child_publishers", network_code)
        return list(self.children)

    def list_sites(self, network_code: str) -> list[GamSite]:
        self._call("list_sites", network_code)
        return list(self.sites.get(network_code, []))

    def list_ad_units(self, network_code: str) -> list[GamAdUnit]:
        self._call("list_ad_units", network_code)
        return list(self.ad_units.get(network_code, []))


@dataclass
class FakeReports:
    """Relatórios prontos por (network, tipo); guarda os períodos pedidos."""

    rows: dict[tuple[str, ReportKind], list[GamReportRow]] = field(default_factory=dict)
    fail_next: list[GamError] = field(default_factory=list)
    calls: list[tuple[str, ReportKind, date, date]] = field(default_factory=list)

    def report(
        self, network_code: str, kind: ReportKind, start: date, end: date
    ) -> list[GamReportRow]:
        self.calls.append((network_code, kind, start, end))
        if self.fail_next:
            raise self.fail_next.pop(0)
        return [row for row in self.rows.get((network_code, kind), []) if start <= row.date <= end]
