"""HTTP Request representation in a python object."""

from typing import TYPE_CHECKING, Any, Generic

from fastlife.domain.model.asgi import ASGIRequest
from fastlife.domain.model.csrf import CSRFToken, create_csrf_token
from fastlife.domain.model.security_policy import TClaimedIdentity, TIdentity
from fastlife.service.registry import TRegistry

if TYPE_CHECKING:
    from fastlife.service.security_policy import (  # coverage: ignore
        AbstractSecurityPolicy,
        HasPermission,
    )


class GenericRequest(ASGIRequest, Generic[TRegistry, TIdentity, TClaimedIdentity]):
    """HTTP Request representation."""

    registry: TRegistry
    """Direct access to the application registry."""
    locale_name: str
    """Request locale used for the i18n of the response."""

    security_policy: (
        "AbstractSecurityPolicy[TRegistry, TIdentity, TClaimedIdentity] | None"
    )
    """Request locale used for the i18n of the response."""

    renderer_globals: dict[str, Any]

    def __init__(self, registry: TRegistry, request: ASGIRequest) -> None:
        super().__init__(request.scope, request.receive)
        self.registry = registry
        self.locale_name = registry.locale_negociator(self)
        self.security_policy = None  # build it from the ? registry
        self.renderer_globals = {}
        self._csrf_token: CSRFToken | None = None

    @property
    def csrf_token(self) -> CSRFToken:
        if self._csrf_token is None:
            name = self.registry.settings.csrf_token_name
            value = self.cookies.get(name) or create_csrf_token()
            self._csrf_token = CSRFToken(name=name, value=value)
        return self._csrf_token

    def add_renderer_globals(self, **kwargs: Any) -> None:
        """
        Add global variables to the template renderer context for the current request.
        """
        self.renderer_globals.update(kwargs)

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
                "explicit fastlife.service.security_policy.InsecurePolicy is required."
            )

        return await self.security_policy.has_permission(permission)
