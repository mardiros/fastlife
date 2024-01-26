from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.by_text("Hello World!", node_name="h1") is not None
    assert resp.html.find("input", {"name": "account.username"}) is not None
    assert resp.html.find("input", {"name": "csrf_token"}) is not None
    resp.form.set("account.username", "Bob")
    resp = resp.form.submit()
    assert resp.by_text("Hello Bob!", node_name="h1") is not None


def test_http_call_optional_form(client: WebTestClient):
    resp = client.get("/autoform")
    input_ = resp.by_label_text("Username")
    assert input_ is not None
    assert input_.attrs["name"] == "payload.username"
    assert input_.attrs["value"] == ""
    assert resp.html.find("input", {"name": "csrf_token"}) is not None

    resp.form.set("payload.username", "Bob")
    resp = resp.form.submit()
    input_ = resp.by_label_text("Username")
    assert input_ is not None
    assert input_.attrs["value"] == "Bob"


def test_session(client: WebTestClient):
    resp = client.get("/login")
    input_ = resp.by_label_text("username")
    assert input_ is not None
    assert input_.attrs["name"] == "payload.username"
    assert input_.attrs["value"] == ""
    assert resp.html.find("input", {"name": "csrf_token"}) is not None

    resp.form.set("payload.username", "Bob")
    resp.form.set("payload.password", "secret")
    resp = resp.form.submit()
    assert resp.by_text("Welcome back Bob!", node_name="h1") is not None


def test_redirect_on_login(client: WebTestClient):
    resp = client.get("/secured", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["Location"] == "http://testserver/login"
