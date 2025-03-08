from typing import Any
from uuid import UUID

import pytest
from fastapi import Request as FastApiRequest

from fastlife import Allowed, Denied, HasPermission, Unauthenticated
from tests.fastlife_app.config import I18nRequest, MyRequest
from tests.fastlife_app.domain.model import AuthnToken
from tests.fastlife_app.views.api.security import MyRegistry
from tests.fastlife_app.views.app.admin.security import SecurityPolicy


@pytest.fixture()
def dummy_request(
    session: dict[str, Any], dummy_registry: MyRegistry
) -> I18nRequest[Any, Any, Any]:
    scope: dict[str, Any] = {
        "type": "http",
        "headers": [("user-agent", "Mozilla/5.0"), ("accept", "text/html")],
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "path": "/",
        "session": session,
    }
    req = I18nRequest[Any, Any, Any](dummy_registry, FastApiRequest(scope))
    return req


@pytest.mark.parametrize(
    "has_permission,expected",
    [
        pytest.param(Allowed, True, id="Allowed"),
        pytest.param(Unauthenticated, False, id="Unauthenticated"),
        pytest.param(Denied, False, id="Forbidden"),
        pytest.param(Allowed("custom reason"), True, id="Allowed(reason)"),
        pytest.param(
            Unauthenticated("custom reason"), False, id="Unauthenticated(reason)"
        ),
        pytest.param(Denied("custom reason"), False, id="Forbidden(reason)"),
    ],
)
def test_has_permission_as_bool(has_permission: HasPermission, expected: bool):
    assert bool(has_permission) is expected


@pytest.mark.parametrize(
    "has_permission,expected",
    [
        pytest.param(Allowed, "Allowed", id="Allowed"),
        pytest.param(Unauthenticated, "Authentication required", id="Unauthenticated"),
        pytest.param(Denied, "Access denied to this resource", id="Forbidden"),
        pytest.param(Allowed("custom reason"), "custom reason", id="Allowed(reason)"),
        pytest.param(
            Unauthenticated("X reasons"), "X reasons", id="Unauthenticated(reason)"
        ),
        pytest.param(Denied("X reasons"), "X reasons", id="Forbidden(reason)"),
    ],
)
def test_has_permission_reason(has_permission: HasPermission, expected: str):
    assert repr(has_permission) == expected


@pytest.mark.parametrize("session", [pytest.param({}, id="anonymous")])
async def test_security_policy_anonymous(dummy_request: MyRequest):
    policy = SecurityPolicy(dummy_request)
    assert (await policy.claimed_identity()) is None
    assert (await policy.identity()) is None


@pytest.mark.parametrize(
    "session",
    [
        pytest.param(
            {
                "user_id": str(UUID(int=1)),
            },
            id="pre_authenticated",
        ),
    ],
)
async def test_security_policy_claimed_identity(dummy_request: MyRequest):
    policy = SecurityPolicy(dummy_request)
    claimed = await policy.claimed_identity()
    assert claimed is not None
    assert claimed.username == "Bob"
    assert await policy.identity() is None


@pytest.mark.parametrize(
    "session",
    [
        pytest.param(
            {
                "authntoken_id": str(UUID(int=11)),
                "user_id": str(UUID(int=1)),
            },
            id="authenticated",
        ),
    ],
)
async def test_security_policy_identity(dummy_request: MyRequest):
    await dummy_request.registry.uow.tokens.add(
        AuthnToken(
            authntoken_id=UUID(int=11),
            user_id=UUID(int=1),
            username="Bob",
            permissions=set(),
        )
    )
    policy = SecurityPolicy(dummy_request)
    ident = await policy.identity()
    assert ident is not None
    assert ident.username == "Bob"
    assert await policy.claimed_identity() is None
