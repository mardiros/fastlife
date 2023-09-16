import pytest
from fastapi import FastAPI

from fastlife import Configurator
from fastlife.testing import WebTestClient


@pytest.fixture
async def app():
    conf = Configurator()
    conf.include("tests.fastlite_app.views")
    return conf.get_app()


@pytest.fixture
def client(app: FastAPI):
    return WebTestClient(app)
