from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.by_text("Hello World", node_name="h1") is not None
