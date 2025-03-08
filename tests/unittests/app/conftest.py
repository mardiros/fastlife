import pytest
from fastapi import FastAPI

from fastlife.testing import WebTestClient
from tests.fastlife_app.entrypoint import MyConfigurator, MySettings
from tests.fastlife_app.service.uow import AbstractUnitOfWork


@pytest.fixture
async def configurator(settings: MySettings) -> MyConfigurator:
    conf = MyConfigurator(settings=settings)
    conf.include("tests.fastlife_app.config")
    conf.include(
        "tests.fastlife_app.views", ignore=[".api", ".app.admin", ".app.insecure"]
    )
    conf.include("tests.fastlife_app.views.api", route_prefix="/api")
    conf.include("tests.fastlife_app.views.app.admin", route_prefix="/admin")
    conf.include("tests.fastlife_app.views.app.insecure", route_prefix="/insecure")
    return conf


@pytest.fixture
async def app(configurator: MyConfigurator):
    yield configurator.build_asgi_app()


@pytest.fixture()
def uow(configurator: MyConfigurator) -> AbstractUnitOfWork:
    return configurator.registry.uow


@pytest.fixture
def client(app: FastAPI, settings: MySettings) -> WebTestClient:
    return WebTestClient(app, settings=settings)
