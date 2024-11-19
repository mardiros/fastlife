from typing import Annotated, Callable
from typing_extensions import Any

from fastapi import Depends
from fastapi import Request as FastAPIRequest

from fastlife import (
    DefaultRegistry,
    GenericConfigurator,
    GenericRequest,
    Settings,
)
from fastlife.config.configurator import configure
from fastlife.config.registry import TRegistry
from fastlife.config.request_factory import RequestFactory
from fastlife.shared_utils.resolver import resolve
from tests.fastlife_app.service.uow import AbstractUnitOfWork


class MySettings(Settings):
    registry_class: str = "tests.fastlife_app.config:MyRegistry"
    uow: str = "tests.fastlife_app.adapters.inmemory_uow:UnitOfWork"


class MyRegistry(DefaultRegistry):
    uow_factory: Callable[..., AbstractUnitOfWork]

    def __init__(self, settings: MySettings) -> None:
        super().__init__(settings)
        self.uow_factory = lambda: resolve(settings.uow)(settings)


class CustomRequest(GenericRequest[TRegistry]):
    uow: AbstractUnitOfWork
    def __init__(self, registry: TRegistry, request: FastAPIRequest) -> None:
        super().__init__(registry, request)
        self.uow = registry.uow_factory()  # type: ignore


def get_request(request: FastAPIRequest) -> CustomRequest[MyRegistry]:
    return request  # type: ignore


MyConfigurator = GenericConfigurator[MyRegistry]
MyRequest = Annotated[CustomRequest[MyRegistry], Depends(get_request)]


class MyRequestFactory(RequestFactory):
    def __init__(self, registry: MyRegistry) -> None:
        super().__init__(registry)
        self.request_cls = MyRequest
