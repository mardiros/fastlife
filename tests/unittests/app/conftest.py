import pytest
from fastapi import FastAPI

from fastlife import Configurator
from fastlife.configurator.configurator import Settings
from fastlife.configurator.registry import cleanup_registry
from fastlife.testing import WebTestClient


@pytest.fixture
async def app():
    conf = Configurator(
        Settings(template_search_path="fastlife:templates,tests.fastlife_app:templates")
    )
    conf.include("tests.fastlife_app.views")
    yield conf.get_app()
    cleanup_registry()


@pytest.fixture
def client(app: FastAPI):
    return WebTestClient(app)
