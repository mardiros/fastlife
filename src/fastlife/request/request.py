"""HTTP Request representation in a python object."""

from typing import TYPE_CHECKING, Any

from fastapi import Request as FastAPIRequest
from fastapi.params import Depends
from typing_extensions import Annotated, Generic

from fastlife.config.registry import AppRegistry, TRegistry

if TYPE_CHECKING:
    from fastlife.security.policy import (  # coverage: ignore
        AbstractSecurityPolicy,
        HasPermission,
    )


class FastLifeRequest(FastAPIRequest, Generic[TRegistry]):
    """HTTP Request representation."""

    registry: TRegistry
    """Direct access to the application registry."""
    locale_name: str
    """Request locale used for the i18n of the response."""

    security_policy: "AbstractSecurityPolicy[Any] | None"
    """Request locale used for the i18n of the response."""

    def __init__(self, registry: TRegistry, request: FastAPIRequest) -> None:
        super().__init__(request.scope, request.receive)
        self.registry = registry
        self.locale_name = registry.locale_negociator(self)
        self.security_policy = None  # build it from the ? registry

    async def has_permission(
        self, permission: str
    ) -> "HasPermission | type[HasPermission]":
        """
        A helper to check that a user has the given permission.

        Not that this method does not raised, it return a boolean like object.
        It allows batch permission checks.
        You might need to check multiple permissions in different contexts or
        for different resources before raising an http error.
        """
        if self.security_policy is None:
            raise RuntimeError(
                f"Request {self.url.path} require a security policy, "
                "explicit fastlife.security.policy.InsecurePolicy is required."
            )

        return await self.security_policy.has_permission(permission)


def get_request(request: FastAPIRequest) -> FastLifeRequest[Any]:
    return request  # type: ignore


GenericRequest = Annotated[FastLifeRequest[TRegistry], Depends(get_request)]
"""
FastAPI handle its Request objects using a lenient_issubclass,
basically a issubclass(Request), doe to the Generic[T], it does not work.
"""

Request = Annotated[FastLifeRequest[AppRegistry], Depends(get_request)]
"""
FastAPI handle its Request objects using a lenient_issubclass,
basically a issubclass(Request), doe to the Generic[T], it does not work.
"""


def get_registry(request: GenericRequest[AppRegistry]) -> AppRegistry:
    return request.registry


Registry = Annotated[AppRegistry, Depends(get_registry)]
"""FastAPI dependency to access to the registry."""
