"""Security policy."""

import abc
from typing import Annotated, Any, Generic

from fastapi import Depends

from fastlife import GenericRequest, get_request
from fastlife.domain.model.security_policy import (
    Allowed,
    Anonymous,
    Authenticated,
    AuthenticationState,
    Forbidden,
    HasPermission,
    MFARequired,
    PendingMFA,
    TClaimedIdentity,
    TIdentity,
    Unauthorized,
)
from fastlife.service.registry import TRegistry


class AbstractSecurityPolicy(abc.ABC, Generic[TRegistry, TIdentity, TClaimedIdentity]):
    """Security policy base class."""

    Forbidden = Forbidden
    """The exception raised if the user identified is not granted."""
    Unauthorized = Unauthorized
    """The exception raised if no user has been identified."""
    MFARequired = MFARequired
    """The exception raised if no user has been authenticated using a MFA."""

    request: GenericRequest[TRegistry, TIdentity, TClaimedIdentity]
    """Request where the security policy is applied."""

    def __init__(
        self,
        request: Annotated[
            GenericRequest[TRegistry, TIdentity, TClaimedIdentity], Depends(get_request)
        ],
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
        self._authentication_state: (
            AuthenticationState[TClaimedIdentity, TIdentity] | None
        ) = None

    async def get_authentication_state(
        self,
    ) -> AuthenticationState[TClaimedIdentity, TIdentity]:
        """
        Return app-specific user object or None.
        """
        if self._authentication_state is None:
            self._authentication_state = await self.build_authentication_state()
        return self._authentication_state

    async def claimed_identity(self) -> TClaimedIdentity | None:
        """
        Return app-specific user object that pretend to be identified.
        """
        auth = await self.get_authentication_state()
        match auth:
            case PendingMFA(claimed):
                return claimed
            case _:
                return None

    async def identity(self) -> TIdentity | None:
        """
        Return app-specific user object after an mfa authentication or None.
        """
        auth = await self.get_authentication_state()
        match auth:
            case Authenticated(identity):
                return identity
            case _:
                return None

    @abc.abstractmethod
    async def build_authentication_state(
        self,
    ) -> AuthenticationState[TClaimedIdentity, TIdentity]:
        """
        Return the authentication state for the current request.
        """

    @abc.abstractmethod
    async def has_permission(
        self, permission: str
    ) -> HasPermission | type[HasPermission]:
        """Allow access to everything if signed in."""

    @abc.abstractmethod
    async def pre_remember(self, claimed_identity: TClaimedIdentity) -> None:
        """Save the user identity in the request session."""

    @abc.abstractmethod
    async def remember(self, identity: TIdentity) -> None:
        """Save the user identity in the request session."""

    @abc.abstractmethod
    async def forget(self) -> None:
        """Destroy the request session."""


class AbstractNoMFASecurityPolicy(AbstractSecurityPolicy[TRegistry, TIdentity, None]):
    async def pre_remember(self, claimed_identity: None) -> None:
        """Do Nothing."""


class InsecurePolicy(AbstractNoMFASecurityPolicy[Any, None]):
    """
    An implementation of the security policy made for explicit unsecured access.

    Setting a permission on a view require a security policy, if not set, accessing
    to a view will raise a RuntimeError. To bypass this error for testing purpose
    or your own reason, the InsecurePolicy has to be set to the configurator.
    """

    async def build_authentication_state(
        self,
    ) -> AuthenticationState[None, None]:
        return Anonymous

    async def has_permission(
        self, permission: str
    ) -> HasPermission | type[HasPermission]:
        """Access is allways granted."""
        return Allowed

    async def remember(self, identity: None) -> None:
        """Do nothing."""

    async def forget(self) -> None:
        """Do nothing."""
