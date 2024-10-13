"""Security policy."""

import abc
import logging
from collections.abc import Callable, Coroutine
from typing import Annotated, Any, Generic, Literal, TypeVar
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from fastlife import GenericRequest, get_request
from fastlife.config.registry import TRegistry

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
    """
    A type used to know if a permission is allowed or not.

    It behave has a boolean, but 3 possibilities exists defind has 3 sub-types
    {class}`Allowed` {class}`Unauthenticated` or {class}`Denied`.

    In many cases Unauthenticated call may redirect to a login page,
    where authenticated user are not redirected. they have an error message,
    or the frontend may use the information to adapt its interface.
    """

    kind: Literal["allowed", "unauthenticated", "denied"]
    reason: str

    def __new__(cls, reason: str) -> "HasPermission":
        instance = super().__new__(cls)
        instance.reason = reason
        return instance

    def __repr__(self) -> str:
        return self.reason

    def __bool__(self) -> bool:
        return self.kind == "allowed"


class Allowed(HasPermission):
    """Represent a permission check result that is allowed."""

    kind = "allowed"
    reason = "Allowed"


class Unauthenticated(HasPermission):
    """
    Represent a permission check result that is not allowed due to
    missing authentication mechanism.
    """

    kind = "unauthenticated"
    reason = "Authentication required"


class Denied(HasPermission):
    """
    Represent a permission check result that is not allowed due to lack of permission.
    """

    kind = "denied"
    reason = "Access denied to this resource"


class AbstractSecurityPolicy(abc.ABC, Generic[TUser, TRegistry]):
    """Security policy base classe."""

    Forbidden = Forbidden
    """The exception raised if the user identified is not granted."""
    Unauthorized = Unauthorized
    """The exception raised if no user has been identified."""

    request: GenericRequest[TRegistry]
    """Request where the security policy is applied."""

    def __init__(
        self, request: Annotated[GenericRequest[TRegistry], Depends(get_request)]
    ):
        """
        Build the security policy.

        When implementing a security policy, multiple parameters can be added
        to the constructor as FastAPI dependencies, using the `Depends` FastAPI
        annotation.
        The security policy is installed has a depenency of the router that hold
        a route prefix of the application.
        """
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


class InsecurePolicy(AbstractSecurityPolicy[None, Any]):
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
