from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.by_text("Hello World!", node_name="h1") is not None
    assert resp.html.find("input", {"name": "name"}) is not None
    assert resp.html.find("input", {"name": "csrf_token"}) is not None
    resp.form.set("name", "Bob")
    resp = resp.form.submit()
    assert resp.by_text("Hello Bob!", node_name="h1") is not None
