"""HTTP Request representation in a python object."""

from typing import TYPE_CHECKING, Any

from fastapi import Request as FastAPIRequest

if TYPE_CHECKING:
    from fastlife.config.registry import AppRegistry  # coverage: ignore
    from fastlife.security.policy import AbstractSecurityPolicy, Allowed, HasPermission


class Request(FastAPIRequest):
    """HTTP Request representation."""

    registry: "AppRegistry"
    """Direct access to the application registry."""
    locale_name: str
    """Request locale used for the i18n of the response."""

    security_policy: "AbstractSecurityPolicy[Any] | None"
    """Request locale used for the i18n of the response."""

    def __init__(self, registry: "AppRegistry", request: FastAPIRequest) -> None:
        super().__init__(request.scope, request.receive)
        self.registry = registry
        self.locale_name = registry.locale_negociator(self)
        self.security_policy = None  # build it from the ? registry

    async def has_permission(
        self, permission: str
    ) -> "HasPermission | type[HasPermission]":
        if self.security_policy:
            return await self.security_policy.has_permission(permission)
        return Allowed
