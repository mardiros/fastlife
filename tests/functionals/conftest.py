import pytest
from fastapi import FastAPI
from fastlife import Configurator
from fastapi.testclient import TestClient


@pytest.fixture
async def app():
    conf = Configurator()
    return conf.get_app()


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
