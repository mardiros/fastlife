from typing import TYPE_CHECKING, Any, Callable, Coroutine

from fastapi import Request as BaseRequest
from fastapi.routing import APIRoute
from starlette.responses import Response
from starlette.types import Receive, Scope

if TYPE_CHECKING:
    from .registry import AppRegistry  # coverage: ignore


class FastlifeRequest(BaseRequest):
    def __init__(self, registry: "AppRegistry", scope: Scope, receive: Receive) -> None:
        super().__init__(scope, receive)
        self.registry = registry


class FastlifeRoute(APIRoute):
    registry: "AppRegistry" = None  # type: ignore

    def get_route_handler(  # type: ignore
        self,
    ) -> Callable[[FastlifeRequest], Coroutine[Any, Any, Response]]:
        orig_route_handler = super().get_route_handler()

        async def route_handler(request: BaseRequest) -> FastlifeRequest:
            req = FastlifeRequest(self.registry, request.scope, request.receive)
            return await orig_route_handler(req)  # type: ignore

        return route_handler  # type: ignore
