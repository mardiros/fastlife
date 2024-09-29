"""HTTP Request representation in a python object."""

from typing import TYPE_CHECKING, Any

from fastapi import Request as FastAPIRequest

if TYPE_CHECKING:
    from fastlife.config.registry import AppRegistry  # coverage: ignore
    from fastlife.security.policy import (  # coverage: ignore
        AbstractSecurityPolicy,
        HasPermission,
    )


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
