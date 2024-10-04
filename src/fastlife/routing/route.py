"""HTTP Route."""

from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any

from fastapi.routing import APIRoute
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response

from fastlife.request.request import Request

if TYPE_CHECKING:
    from fastlife.config.registry import DefaultRegistry  # coverage: ignore


class Route(APIRoute):
    """
    Routing for fastlife application.

    The fastlife router construct fastlife request object in order to
    have the registry property available in every received request.
    """

    _registry: "DefaultRegistry"
    """
    The application registry.

    this static variable is initialized by the configurator during
    the startup and keep the registry during the lifetime of the application.

    this variable should be accessed via the request object or the
    {class}`fastlife.config.Registry` depenency injection.
    """

    def get_route_handler(
        self,
    ) -> Callable[[StarletteRequest], Coroutine[Any, Any, Response]]:
        """
        Replace the request object by the fastlife request associated with the registry.
        """
        orig_route_handler = super().get_route_handler()

        async def route_handler(request: StarletteRequest) -> Response:
            req = Request(self._registry, request)
            return await orig_route_handler(req)

        return route_handler
