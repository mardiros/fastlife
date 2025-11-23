"""HTTP Route."""

from collections.abc import Callable, Coroutine
from typing import Any

from fastapi.routing import APIRoute

from fastlife.domain.model.asgi import ASGIRequest, ASGIResponse


class Route(APIRoute):
    """
    Routing for fastlife application.

    The fastlife router construct fastlife request object in order to
    have the registry property available in every received request.
    """

    def get_route_handler(
        self,
    ) -> Callable[[ASGIRequest], Coroutine[Any, Any, ASGIResponse]]:
        """
        Replace the request object by the fastlife request associated with the registry.
        """
        orig_route_handler = super().get_route_handler()

        async def route_handler(request: ASGIRequest) -> ASGIResponse:
            req = request.scope["fastlife.registry"].request_factory(request)
            return await orig_route_handler(req)

        return route_handler
