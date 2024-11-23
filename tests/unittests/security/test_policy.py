import pytest

from fastlife.domain.model.security_policy import HasPermission
from tests.fastlife_app.views.app.admin.security import Allowed, Denied, Unauthenticated


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
