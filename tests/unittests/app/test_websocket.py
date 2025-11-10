import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def wsclient(app: FastAPI):
    return TestClient(app, headers={"Authorization": "Bearer abc"})


def test_websocket(wsclient: TestClient):
    with wsclient.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
