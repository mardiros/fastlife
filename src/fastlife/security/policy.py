"""Security policy."""

import abc
import logging
from typing import Any, Callable, Coroutine, Literal, TypeVar
from uuid import UUID

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing_extensions import Generic

from fastlife import Request


CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]

TUser = TypeVar("TUser")

log = logging.getLogger(__name__)


class Unauthorized(HTTPException):
    """An exception raised to stop a request exectution and return an HTTP Error."""

    def __init__(
        self,
        status_code: int = HTTP_401_UNAUTHORIZED,
        detail: str = "Unauthorized",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class Forbidden(HTTPException):
    """An exception raised to stop a request exectution and return an HTTP Error."""

    def __init__(
        self,
        status_code: int = HTTP_403_FORBIDDEN,
        detail: str = "Forbidden",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class BoolMeta(type):
    def __bool__(cls) -> bool:
        return cls.kind == "allowed"  # type: ignore

    def __repr__(cls) -> str:
        return cls.reason  # type: ignore


class HasPermission(int, metaclass=BoolMeta):
    kind: Literal["allowed", "unauthenticated", "denied"]
    reason: str

    def __new__(cls, reason: str) -> "HasPermission":
        instance = super().__new__(cls)
        instance.reason = reason
        return instance

    def __repr__(self) -> str:
        return self.reason


class Allowed(HasPermission):
    kind = "allowed"
    reason = "Allowed"


class Unauthenticated(HasPermission):
    kind = "unauthenticated"
    reason = "Authentication required"


class Denied(HasPermission):
    kind = "denied"
    reason = "Access denied to resource"


class AbstractSecurityPolicy(abc.ABC, Generic[TUser]):
    Forbidden = Forbidden
    Unauthorized = Unauthorized

    def __init__(self, request: "Request"):
        self.request = request
        self.request.security_policy = self  # we do backref to implement has_permission

    @abc.abstractmethod
    async def identity(self) -> TUser | None:
        """
        Return app-specific user object or raise an HTTPException.
        """

    @abc.abstractmethod
    async def authenticated_userid(self) -> str | UUID | None:
        """
        Return app-specific user object or raise an HTTPException.
        """

    @abc.abstractmethod
    async def has_permission(
        self, permission: str
    ) -> HasPermission | type[HasPermission]:
        """Allow access to everything if signed in."""

    @abc.abstractmethod
    async def remember(self, user: TUser) -> None:
        """Save the user identity in the request session."""

    @abc.abstractmethod
    async def forget(self) -> None:
        """Destroy the request session."""


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given permission_name.

    This method has to be overriden using the setting
    :attr:`fastlife.config.settings.Settings.check_permission` to implement it.

    When the check permission is properly set in the settings., the hook is called
    for every route added with a permission keyword.
    {meth}`fastlife.config.configurator.Configurator.add_route`

    :param permission_name: a permission name set in a view to check access.
    :return: a function that raise http exceptions or any configured exception here.
    """

    async def depencency_injection(request: Request) -> None:
        if request.security_policy is None:
            raise RuntimeError(
                f"Request {request.url} require a security policy, "
                "explicit fastlife.security.policy.InsecurePolicy is required"
            )
        allowed = await request.security_policy.has_permission(permission_name)
        match allowed.kind:
            case "allowed":
                return
            case "denied":
                raise request.security_policy.Forbidden(detail=allowed.reason)
            case "unauthenticated":
                raise request.security_policy.Unauthorized(detail=allowed.reason)

    return depencency_injection


class InsecurePolicy(AbstractSecurityPolicy[None]):
    async def identity(self) -> None:
        return None

    async def authenticated_userid(self) -> str | UUID:
        return UUID(int=0)

    async def has_permission(
        self, permission: str
    ) -> HasPermission | type[HasPermission]:
        """Allow access to everything if signed in."""
        return Allowed

    async def remember(self, user: None) -> None:
        """Save the user identity in the request session."""
        raise RuntimeError("a SecurityPolicy must be set to remember users")

    async def forget(self) -> None:
        """Destroy the request session."""
