"""HTTP Request representation in a python object."""
from typing import TYPE_CHECKING

from fastapi import Request as BaseRequest

if TYPE_CHECKING:
    from fastlife.config.registry import AppRegistry  # coverage: ignore


class Request(BaseRequest):
    """HTTP Request representation."""

    registry: "AppRegistry"
    """Direct access to the application registry."""

    def __init__(self, registry: "AppRegistry", request: BaseRequest) -> None:
        super().__init__(request.scope, request.receive)
        self.registry = registry
