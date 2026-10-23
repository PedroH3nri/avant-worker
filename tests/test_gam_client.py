import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest
from avant_core.gam.domain import Delegation, InventoryStatus
from avant_core.ports import GamAccessDenied, GamError, GamNetworkNotFound, GamUnavailable
from google.auth.credentials import Credentials

from avant_worker.gam_client import BASE_URL, RestGamClient

Handler = Callable[[httpx.Request], httpx.Response]


class FakeCredentials(Credentials):
    def __init__(self) -> None:
        super().__init__()  # type: ignore[no-untyped-call]

    def refresh(self, request: Any) -> None:
        self.token = "token-de-teste"


def client(handler: Handler) -> tuple[RestGamClient, list[httpx.Request]]:
    seen: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return handler(request)

    http = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(record))
    gam = RestGamClient(FakeCredentials(), service_account_email="avant@groone.iam", http=http)
    return gam, seen


def ok(body: dict[str, Any]) -> httpx.Response:
    return httpx.Response(200, json=body)


def test_network_and_admin_check() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/networks/123":
            return ok({"networkCode": "123", "displayName": "Açaí", "testNetwork": False})
        assert request.url.path == "/v1/networks/123/users/me"
        return ok({"email": "avant@groone.iam", "role": "networks/123/roles/-1", "active": True})

    gam, seen = client(handler)
    info = gam.get_network("123")
    assert (info.network_code, info.display_name, info.is_test) == ("123", "Açaí", False)
    assert gam.is_admin("123")
    assert seen[0].headers["authorization"] == "Bearer token-de-teste"
    assert gam.service_account_email == "avant@groone.iam"


def test_not_admin_when_role_is_other_or_user_inactive() -> None:
    answers = iter(
        [
            {"role": "-5", "active": True},
            {"role": "-1", "active": False},
        ]
    )
    gam, _ = client(lambda r: ok(next(answers)))
    assert not gam.is_admin("123")
    assert not gam.is_admin("123")


def test_sites_follow_pages() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["pageSize"] == "1000"
        if "pageToken" not in request.url.params:
            return ok(
                {
                    "sites": [
                        {
                            "name": "networks/9/sites/1",
                            "url": "acai.com.br",
                            "approvalStatus": "APPROVED",
                            "childNetworkCode": "123",
                        }
                    ],
                    "nextPageToken": "p2",
                }
            )
        assert request.url.params["pageToken"] == "p2"
        return ok({"sites": [{"name": "networks/9/sites/2", "url": "b.com"}]})

    gam, seen = client(handler)
    sites = list(gam.list_sites("9"))
    assert [(s.gam_id, s.url, s.child_network_code) for s in sites] == [
        ("1", "acai.com.br", "123"),
        ("2", "b.com", None),
    ]
    assert sites[1].approval_status is None and len(seen) == 2


def test_ad_units_without_root_and_archived() -> None:
    body = {
        "adUnits": [
            {"name": "networks/9/adUnits/100", "displayName": "9"},  # raiz
            {
                "name": "networks/9/adUnits/1",
                "parentAdUnit": "networks/9/adUnits/100",
                "displayName": "acai.com.br",
                "status": "ACTIVE",
            },
            {
                "name": "networks/9/adUnits/2",
                "parentAdUnit": "networks/9/adUnits/1",
                "displayName": "topo",
                "adUnitCode": "acai_topo",
                "status": "INACTIVE",
            },
            {
                "name": "networks/9/adUnits/3",
                "parentAdUnit": "networks/9/adUnits/1",
                "displayName": "velho",
                "status": "ARCHIVED",
            },
        ]
    }
    gam, _ = client(lambda r: ok(body))
    units = list(gam.list_ad_units("9"))
    assert [(u.gam_id, u.parent_gam_id, u.code, u.status) for u in units] == [
        ("1", None, None, InventoryStatus.ACTIVE),
        ("2", "1", "acai_topo", InventoryStatus.INACTIVE),
    ]


def test_child_publishers() -> None:
    body = {
        "childPublishers": [
            {
                "name": "networks/9/childPublishers/7",
                "childNetwork": "networks/123",
                "displayName": "Açaí",
                "email": "dono@acai.com.br",
                "delegationType": "MANAGE_INVENTORY",
                "accountStatus": "APPROVED",
            },
            {"name": "networks/9/childPublishers/8", "email": "x@y.com"},  # sem network ainda
        ]
    }
    gam, _ = client(lambda r: ok(body))
    (child,) = gam.list_child_publishers("9")
    assert child.network_code == "123" and child.delegation is Delegation.MANAGE_INVENTORY
    assert child.account_status == "APPROVED" and child.email == "dono@acai.com.br"


@pytest.mark.parametrize(
    ("status", "error"),
    [
        (401, GamAccessDenied),
        (403, GamAccessDenied),
        (404, GamNetworkNotFound),
        (429, GamUnavailable),
        (503, GamUnavailable),
        (400, GamError),
    ],
)
def test_http_errors_are_classified(status: int, error: type[GamError]) -> None:
    body = {"error": {"code": status, "message": "detalhe do Google"}}
    gam, _ = client(lambda r: httpx.Response(status, content=json.dumps(body)))
    with pytest.raises(error) as raised:
        gam.get_network("123")
    assert type(raised.value) is error and "detalhe do Google" in str(raised.value)
    assert raised.value.permanent is (error is not GamUnavailable)


def test_network_failures_are_temporary() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("lento", request=request)

    gam, _ = client(handler)
    with pytest.raises(GamUnavailable):
        gam.get_network("123")
