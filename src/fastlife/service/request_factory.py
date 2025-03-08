"""Find the localization gor the given request."""

from collections.abc import Callable
from typing import Any

from starlette.requests import Request as StarletteRequest

from fastlife.domain.model.request import GenericRequest
from fastlife.service.registry import DefaultRegistry, TRegistry

RequestFactory = Callable[[StarletteRequest], GenericRequest[Any, Any, Any]]
"""Transform the Startlette request object to the faslife version."""

RequestFactoryBuilder = Callable[[TRegistry], RequestFactory]
"""Interface to implement to create a request factory"""


def default_request_factory(registry: DefaultRegistry) -> RequestFactory:
    """The default local negociator return the locale set in the conf."""

    def request(request: StarletteRequest) -> GenericRequest[Any, Any, Any]:
        return GenericRequest[Any, Any, Any](registry, request)

    return request
