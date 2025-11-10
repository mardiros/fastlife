import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def wsclient(app: FastAPI):
    return TestClient(app, headers={"Authorization": "Bearer abc"})


def test_websocket_json(wsclient: TestClient):
    with wsclient.websocket_connect("/ws/json") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello testserver.local"}
        websocket.send_json({"msg": "Hello from test"})
        data = websocket.receive_json()
        assert data == {"msg": "Hello from test"}


def test_websocket_text(wsclient: TestClient):
    with wsclient.websocket_connect("/ws/text") as websocket:
        data = websocket.receive_text()
        assert data == "Hello testserver.local"
        websocket.send_text("Hello from test")
        data = websocket.receive_text()
        assert data == "Hello from test"


def test_websocket_bytes(wsclient: TestClient):
    with wsclient.websocket_connect("/ws/bytes") as websocket:
        data = websocket.receive_bytes()
        assert data == b"Hello testserver.local"
        websocket.send_bytes(b"Hello from test")
        data = websocket.receive_bytes()
        assert data == b"Hello from test"
