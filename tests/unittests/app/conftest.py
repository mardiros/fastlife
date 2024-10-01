import pytest
from fastapi import FastAPI

from fastlife import Configurator
from fastlife.config.configurator import Settings
from fastlife.testing import WebTestClient


@pytest.fixture
async def app(settings: Settings):
    conf = Configurator(settings=settings)
    conf.include(
        "tests.fastlife_app.views", ignore=[".api", ".app.admin", ".app.insecure"]
    )
    conf.include("tests.fastlife_app.views.api", route_prefix="/api")
    conf.include("tests.fastlife_app.views.app.admin", route_prefix="/admin")
    conf.include("tests.fastlife_app.views.app.insecure", route_prefix="/insecure")
    yield conf.build_asgi_app()


@pytest.fixture
def client(app: FastAPI, settings: Settings):
    return WebTestClient(app, settings=settings)
