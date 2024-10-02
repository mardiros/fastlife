from typing import Annotated

from fastapi import Depends

from fastlife import (
    DefaultRegistry,
    GenericConfigurator,
    GenericRequest,
    Settings,
    get_request,
)
from fastlife.shared_utils.resolver import resolve
from tests.fastlife_app.service.uow import AbstractUnitOfWork


class MySettings(Settings):
    registry_class: str = "tests.fastlife_app.config:MyRegistry"
    uow: str = "tests.fastlife_app.adapters.inmemory_uow:UnitOfWork"


class MyRegistry(DefaultRegistry):
    uow: AbstractUnitOfWork

    def __init__(self, settings: MySettings) -> None:
        super().__init__(settings)
        self.uow = resolve(settings.uow)(settings)


MyConfigurator = GenericConfigurator[MyRegistry]
MyRequest = Annotated[GenericRequest[MyRegistry], Depends(get_request)]
