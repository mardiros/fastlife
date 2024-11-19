"""Customize the request class."""

from typing import TYPE_CHECKING, Any

from starlette.requests import Request as StarletteRequest

from fastlife.shared_utils.resolver import resolve

if TYPE_CHECKING:
    from fastlife.request.request import GenericRequest
    from fastlife.config.registry import GenericRegistry


class RequestFactory:
    """
    Build the request object based on the Starlet request instance.

    :param registry: application registry
    :param request_cls: class instanciated when the factory is called
    """

    def __init__(self, registry: "GenericRegistry[Any]") -> None:
        self.request_cls = resolve(registry.settings.request_class)
        self.registry = registry

    def __call__(self, request: "StarletteRequest") -> "GenericRequest[Any]":
        return self.request_cls(self.registry, request)
