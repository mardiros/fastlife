from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI

from fastlife import (
    GenericConfigurator,
    GenericRegistry,
    GenericRequest,
    Settings,
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
MyRequest = Annotated[
    GenericRequest[MyRegistry, AuthnToken, UserAccount], Depends(get_request)
]
