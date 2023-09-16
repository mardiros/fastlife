from fastapi.testclient import TestClient


def test_http_call(client: TestClient):
    resp = client.get("/")
    assert "Hello World" in resp.text
