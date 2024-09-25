"""HTTP Request representation in a python object."""

from typing import TYPE_CHECKING

from fastapi import Request as FastAPIRequest

if TYPE_CHECKING:
    from fastlife.config.registry import AppRegistry  # coverage: ignore


class Request(FastAPIRequest):
    """HTTP Request representation."""

    registry: "AppRegistry"
    """Direct access to the application registry."""
    locale_name: str
    """Request locale used for the i18n of the response."""

    def __init__(self, registry: "AppRegistry", request: FastAPIRequest) -> None:
        super().__init__(request.scope, request.receive)
        self.registry = registry
        self.locale_name = registry.locale_negociator(self)
