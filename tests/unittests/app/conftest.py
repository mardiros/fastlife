import pytest
from fastapi import FastAPI

from fastlife import Configurator
from fastlife.configurator.configurator import Settings
from fastlife.configurator.registry import cleanup_registry
from fastlife.testing import WebTestClient


@pytest.fixture
async def app(settings: Settings):
    conf = Configurator(settings=settings)
    conf.include("tests.fastlife_app.views")
    yield conf.get_app()
    cleanup_registry()


@pytest.fixture
def client(app: FastAPI, settings: Settings):
    return WebTestClient(app, settings=settings)
