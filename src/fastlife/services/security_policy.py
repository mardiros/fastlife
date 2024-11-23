"""Security policy."""

from collections.abc import Callable, Coroutine
from typing import Any

"""Security policy."""

import abc
from typing import Annotated, Generic
from uuid import UUID

from fastapi import Depends

from fastlife import GenericRequest, get_request
from fastlife.domain.model.security_policy import (
    Allowed,
    Forbidden,
    HasPermission,
    TUser,
    Unauthorized,
)
from fastlife.services.registry import TRegistry


class AbstractSecurityPolicy(abc.ABC, Generic[TUser, TRegistry]):
    """Security policy base class."""

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


CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given permission_name.

    Adding a permission on the route requires that a security policy has been
    added using the method
    {meth}`fastlife.config.configurator.GenericConfigurator.set_security_policy`

    :param permission_name: a permission name set in a view to check access.
    :return: a function that raise http exceptions or any configured exception here.
    """
    # the check_permission is called by the configurator
    # and the request is exposed in the public module creating a circular dependency.
    from fastlife import Request  # a type must be resolved to inject a dependency.

    async def depencency_injection(request: Request) -> None:
        if request.security_policy is None:
            raise RuntimeError(
                f"Request {request.url.path} require a security policy, "
                "explicit fastlife.services.security_policy.InsecurePolicy is required"
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
