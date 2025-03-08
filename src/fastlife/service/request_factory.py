"""Customize the request class."""

from collections.abc import Callable
from typing import Any

from fastlife.domain.model.asgi import ASGIRequest
from fastlife.domain.model.request import GenericRequest
from fastlife.service.registry import DefaultRegistry, TRegistry

RequestFactory = Callable[[ASGIRequest], GenericRequest[Any, Any, Any]]
"""
Transform the [ASGIRequest](#fastlife.domain.model.asgi.ASGIRequest)
object to the fastlife [GenericRequest](#fastlife.domain.model.request.GenericRequest).
"""

RequestFactoryBuilder = Callable[[TRegistry], RequestFactory]
"""Interface to implement to create a request factory"""


def default_request_factory(registry: DefaultRegistry) -> RequestFactory:
    """The default request factory the return the generic request."""

    def request(request: ASGIRequest) -> GenericRequest[Any, Any, Any]:
        return GenericRequest[Any, Any, Any](registry, request)

    return request
