"""Security policy."""

import abc
import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal, TypeVar
from uuid import UUID

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing_extensions import Generic

if TYPE_CHECKING:
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


class InsecurePolicy(AbstractSecurityPolicy[None]):
    """
    An implementation of the security policy made for explicit unsecured access.

    Setting a permission on a view require a security policy, if not set, accessing
    to a view will raise a RuntimeError. To bypass this error for testing purpose
    or your own reason, the InsecurePolicy has to be set to the configurator.
    """

    async def identity(self) -> None:
        """Nobodies is identified."""
        return None

    async def authenticated_userid(self) -> str | UUID:
        """An uuid mades of 0."""
        return UUID(int=0)

    async def has_permission(
        self, permission: str
    ) -> HasPermission | type[HasPermission]:
        """Access is allways granted."""
        return Allowed

    async def remember(self, user: None) -> None:
        """Do nothing."""

    async def forget(self) -> None:
        """Do nothing."""


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given permission_name.

    Adding a permission on the route requires that a security policy has been
    added using the method
    {meth}`fastlife.config.configurator.Configurator.set_security_policy`

    :param permission_name: a permission name set in a view to check access.
    :return: a function that raise http exceptions or any configured exception here.
    """
    from fastlife import Request  # a type must be resolved to inject a dependency.

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
