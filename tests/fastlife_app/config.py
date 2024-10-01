from typing import Annotated
from fastapi import Depends
from fastlife.config.configurator import GenericConfigurator, Settings
from fastlife.config.registry import AppRegistry
from fastlife.request import GenericRequest, get_request
from tests.fastlife_app.services.uow import UnitOfWork


class MySettings(Settings):
    foobar: str
    registry_class: str = "tests.fastlife_app.config:MyRegistry"


class MyRegistry(AppRegistry):
    uow: UnitOfWork

    def __init__(self, settings: MySettings) -> None:
        super().__init__(settings)
        self.uow = UnitOfWork()


MyConfigurator = GenericConfigurator[MyRegistry]
MyRequest = Annotated[GenericRequest[MyRegistry], Depends(get_request)]
