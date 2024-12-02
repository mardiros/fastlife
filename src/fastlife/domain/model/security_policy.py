"""Security policy."""

import logging
from collections.abc import Callable, Coroutine
from typing import Any, Generic, Literal, TypeVar

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]

TClaimedIdentity = TypeVar("TClaimedIdentity")
TIdentity = TypeVar("TIdentity")

log = logging.getLogger(__name__)


class _Anonymous: ...


Anonymous = _Anonymous()
"""
The user is not authenticated.
"""


class PendingMFA(Generic[TClaimedIdentity]):
    """
    The user provided its identity, usually validated with a first factor,
    such as a password but it has not totally proved its authentication
    by a second or many other factors of authentication.
    The type TClaimedIdentity will store the relevant informations during
    this authentication phase.
    """

    claimed: TClaimedIdentity | None
    __match_args__ = ("claimed",)

    def __init__(self, claimed: TClaimedIdentity) -> None:
        self.claimed = claimed


class Authenticated(Generic[TIdentity]):
    """The identity has been validated."""

    __match_args__ = ("identity",)

    def __init__(self, identity: TIdentity) -> None:
        self.identity = identity


AuthenticationState = (
    _Anonymous | PendingMFA[TClaimedIdentity] | Authenticated[TIdentity]
)
"""
Type representing the state of an authentication.
"""

NoMFAAuthenticationState = AuthenticationState[None, TIdentity]
"""
Type representing a state of authentication when no multiple factor of authentication
is involved.
"""


class Unauthorized(HTTPException):
    """An exception raised to stop a request execution and return a 401 HTTP Error."""

    def __init__(
        self,
        status_code: int = HTTP_401_UNAUTHORIZED,
        detail: str = "Unauthorized",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class MFARequired(Unauthorized):
    """
    An exception raised to stop a request execution and return a 401 HTTP Error for MFA.
    """

    def __init__(
        self,
        status_code: int = HTTP_401_UNAUTHORIZED,
        detail: str = "MFA Required",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class Forbidden(HTTPException):
    """An exception raised to stop a request execution and return a 403 HTTP Error."""

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

    kind: Literal["allowed", "unauthenticated", "mfa_required", "denied"]
    """
    Identified basic information of the response.
    It distinguished unauthenticated and denied to eventually raised 401 over 403 error.
    """
    reason: str
    """A human explanation of the response."""

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


class PreAuthenticated(HasPermission):
    """
    Represent a permission check result that is not allowed due to
    missing secondary authentication mechanism.
    """

    kind = "mfa_required"
    reason = "MFA required"


class Denied(HasPermission):
    """
    Represent a permission check result that is not allowed due to lack of permission.
    """

    kind = "denied"
    reason = "Access denied to this resource"
