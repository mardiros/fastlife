from fastlife.testing import WebTestClient


def test_backend_tag(client: WebTestClient):
    resp = client.get("/")
    assert resp.headers["x-backend-tag"] == "dummy-server"
