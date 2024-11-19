import pytest
from fastapi import FastAPI

from fastlife.testing import WebTestClient
from tests.fastlife_app.config import MyRequestFactory
from tests.fastlife_app.entrypoint import MyConfigurator, MySettings


@pytest.fixture
async def app(settings: MySettings):
    conf = MyConfigurator(settings=settings)
    conf.set_request_factory(MyRequestFactory)
    conf.include(
        "tests.fastlife_app.views", ignore=[".api", ".app.admin", ".app.insecure"]
    )
    conf.include("tests.fastlife_app.views.api", route_prefix="/api")
    conf.include("tests.fastlife_app.views.app.admin", route_prefix="/admin")
    conf.include("tests.fastlife_app.views.app.insecure", route_prefix="/insecure")
    yield conf.build_asgi_app()


@pytest.fixture
def client(app: FastAPI, settings: MySettings):
    return WebTestClient(app, settings=settings)
