import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastlife import Configurator


@pytest.fixture
async def app():
    conf = Configurator()
    conf.include("tests.fastlite_app.views")
    return conf.get_app()


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
