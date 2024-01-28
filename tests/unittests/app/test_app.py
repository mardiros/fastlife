from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.by_text("Hello World!", node_name="h1") is not None
    assert "account.username" in resp.form
    assert "csrf_token" in resp.form
    resp.form.set("account.username", "Bob")
    resp = resp.form.submit()
    assert resp.by_text("Hello Bob!", node_name="h1") is not None


def test_http_call_optional_form(client: WebTestClient):
    resp = client.get("/autoform")
    input_ = resp.by_label_text("Username")
    assert input_ is not None
    assert input_.attrs["name"] == "payload.username"
    assert input_.attrs["value"] == ""
    assert "csrf_token" in resp.form

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

    assert "csrf_token" in resp.form
    resp.form.set("payload.username", "Bob")
    resp.form.set("payload.password", "secret")
    resp = resp.form.submit()
    assert resp.by_text("Welcome back Bob!", node_name="h1") is not None

    logout = resp.by_text("logout")
    assert logout is not None, resp.html
    logout.click()


def test_forbidden(client: WebTestClient):
    resp = client.get("/login")
    input_ = resp.by_label_text("username")
    assert input_ is not None
    assert input_.attrs["name"] == "payload.username"
    assert input_.attrs["value"] == ""
    assert "csrf_token" in resp.form

    resp.form.set("payload.username", "Roger")
    resp.form.set("payload.password", "secret")
    resp = resp.form.submit()
    assert resp.status_code == 403


def test_redirect_on_login(client: WebTestClient):
    resp = client.get("/secured", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["Location"] == "http://testserver.local/login"


def test_redirect_on_logout(client: WebTestClient):
    client.session["user_id"] = "2"
    resp = client.get("/secured", follow_redirects=False)
    assert resp.status_code == 200
    logout = resp.by_text("logout")
    assert logout is not None, resp.html
    logout.click()
    assert client.session == {}
