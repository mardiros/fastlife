import pytest

from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/")
    assert resp.html.h1.text == "Hello World!"
    assert "person.nick" in resp.form
    assert "csrf_token" in resp.form
    resp.form.set("person.nick", "Bob")
    resp = resp.form.submit()
    assert resp.html.h1.text == "Hello Bob!"


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
    assert len(resp.html.h2) == 1
    assert resp.html.h2[0].text == "Let's authenticate"
    assert resp.html.hx_target is None
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
    resp = logout.click()
    assert client.session == {}
    assert repr(resp.html) == "<[document]>"
    assert (
        str(resp.html.get_all_by_text("Hello World")[0])
        == '<h1 class="block font-bold font-sans leading-tight pb-4 text-5xl '
        'text-neutral-900 tracking-tight dark:text-white md:text-4xl">Hello World!</h1>'
    )


def test_exception_handler_with_template(client: WebTestClient):
    resp = client.get("/failed-good")
    assert resp.status_code == 500
    assert resp.html.h2[0].text == "Internal Server Error"
    assert resp.content_type == "text/html"


def test_exception_handler_runtime_error(client: WebTestClient):
    with pytest.raises(RuntimeError) as exc:
        client.get("/failed-bad")
    assert str(exc.value) == (
        "No template set for "
        "tests.fastlife_app.views.failed:MyBadException but "
        "tests.fastlife_app.views.failed:my_bad_handler did not return a Response"
    )


def test_exception_handler_raw_response(client: WebTestClient):
    resp = client.get("/failed-ugly")
    assert resp.text == "It's a trap"
    assert resp.content_type == "text/plain"
    assert resp.status_code == 400


def test_exception_handler_custom_status_code(client: WebTestClient):
    resp = client.get("/your-fault")
    assert resp.html.h2[0].text == "Invalid Parameter"
    assert resp.content_type == "text/html"
    assert resp.status_code == 422
