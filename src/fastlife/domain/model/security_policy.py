"""Security policy."""

import logging
from collections.abc import Callable, Coroutine
from typing import Any, Literal, TypeVar

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

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


class Denied(HasPermission):
    """
    Represent a permission check result that is not allowed due to lack of permission.
    """

    kind = "denied"
    reason = "Access denied to this resource"
