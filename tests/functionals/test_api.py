from fastapi.testclient import TestClient


def test_http_call(client: TestClient):
    resp = client.get("/")
    assert "Not Found" in resp.text
