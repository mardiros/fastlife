from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from starlette.datastructures import URL

from fastlife import (
    GenericConfigurator,
    GenericRegistry,
    GenericRequest,
    Settings,
    configure,
    get_request,
)
from fastlife.domain.model.security_policy import TClaimedIdentity, TIdentity
from fastlife.service.registry import TRegistry
from fastlife.service.request_factory import RequestFactory, StarletteRequest
from fastlife.shared_utils.resolver import resolve
from tests.fastlife_app.service.uow import AbstractUnitOfWork


class MySettings(Settings):
    registry_class: str = "tests.fastlife_app.config:MyRegistry"
    uow: str = "tests.fastlife_app.adapters.inmemory_uow:UnitOfWork"


class MyRegistry(GenericRegistry[MySettings]):
    uow: AbstractUnitOfWork
    running: bool = False

    def __init__(self, settings: MySettings) -> None:
        super().__init__(settings)
        self.uow = resolve(settings.uow)(settings)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[Any]:
        MyRegistry.running = True
        async with super().lifespan(app) as x:
            yield x
        MyRegistry.running = False


MyConfigurator = GenericConfigurator[MyRegistry]


class I18nRequest(GenericRequest[TRegistry, TIdentity, TClaimedIdentity]):
    def localized_url_for(self, name: str, /, **path_params: Any) -> URL:
        return self.url_for(name, locale=self.locale_name, **path_params)


MyRequest = Annotated[
    I18nRequest[TRegistry, TIdentity, TClaimedIdentity], Depends(get_request)
]


def request_factory(registry: MyRegistry) -> RequestFactory:
    def request(request: StarletteRequest) -> GenericRequest[Any, Any, Any]:
        return I18nRequest(registry, request)

    return request


@configure
def includeme(config: MyConfigurator):
    config.set_request_factory(request_factory)
