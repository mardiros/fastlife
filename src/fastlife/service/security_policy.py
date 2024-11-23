"""Security policy."""

import abc
from typing import Annotated, Any, Generic
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
from fastlife.service.registry import TRegistry


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
