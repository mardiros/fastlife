from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI

from fastlife import (
    ASGIRequest,
    GenericConfigurator,
    GenericRegistry,
    GenericRequest,
    RequestFactory,
    Settings,
    TClaimedIdentity,
    TIdentity,
    TRegistry,
    configure,
    get_request,
)
from fastlife.shared_utils.resolver import resolve
from tests.fastlife_app.domain.model import AuthnToken, UserAccount
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
    def url_path_for(self, name: str, /, **path_params: Any) -> str:
        return super().url_path_for(name, locale=self.locale_name, **path_params)


MyRequest = Annotated[
    I18nRequest[MyRegistry, AuthnToken, UserAccount], Depends(get_request)
]


def request_factory(registry: MyRegistry) -> RequestFactory:
    def request(request: ASGIRequest) -> GenericRequest[Any, Any, Any]:
        return I18nRequest(registry, request)

    return request


@configure
def includeme(config: MyConfigurator):
    config.set_request_factory(request_factory)
