from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.by_text("Hello World!", node_name="h1") is not None
    assert resp.html.find("input", {"name": "payload.name"}) is not None
    assert resp.html.find("input", {"name": "csrf_token"}) is not None
    resp.form.set("payload.name", "Bob")
    resp = resp.form.submit()
    assert resp.by_text("Hello Bob!", node_name="h1") is not None


def test_http_call_optional_form(client: WebTestClient):
    resp = client.get("/autoform")
    input_ = resp.by_label_text("name")
    assert input_ is not None
    assert input_.attrs["name"] == "payload.name"
    assert input_.attrs["value"] == ""
    assert resp.html.find("input", {"name": "csrf_token"}) is not None

    resp.form.set("payload.name", "Bob")
    resp = resp.form.submit()
    input_ = resp.by_label_text("name")
    assert input_ is not None
    assert input_.attrs["value"] == "Bob"
