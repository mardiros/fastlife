from typing import Generic

from fastlife import Configurator, configure
from fastlife.domain.model.asgi import ASGIApp, Receive, Scope, Send
from fastlife.middlewares.base import AbstractMiddleware
from fastlife.service.registry import GenericRegistry, TSettings


class RegistryMiddleware(AbstractMiddleware, Generic[TSettings]):
    def __init__(self, app: ASGIApp, *, registry: GenericRegistry[TSettings]) -> None:
        self.app = app
        self._registry: GenericRegistry[TSettings] = registry

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Called every time an http request is reveived.

        This method before the request object even exists.
        """
        scope["fastlife.registry"] = self._registry
        await self.app(scope, receive, send)


@configure
def includeme(config: Configurator) -> None:
    config.add_middleware(RegistryMiddleware, registry=config.registry)
