from collections.abc import Mapping

import pytest
from httpx import Response

from fastlife.testing.testclient import WebResponse, WebTestClient


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(Response(status_code=200), 200, id="200"),
        pytest.param(Response(status_code=301), 301, id="301"),
        pytest.param(Response(status_code=302), 302, id="302"),
        pytest.param(Response(status_code=404), 404, id="404"),
    ],
)
def test_status(client: WebTestClient, response: Response, expected: int):
    wr = WebResponse(client, origin="", response=response)
    assert wr.status_code == expected


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(Response(status_code=200), False, id="200"),
        pytest.param(Response(status_code=301), True, id="301"),
        pytest.param(Response(status_code=302), True, id="302"),
        pytest.param(Response(status_code=404), False, id="404"),
    ],
)
def test_is_redirect(client: WebTestClient, response: Response, expected: bool):
    wr = WebResponse(client, origin="", response=response)
    assert wr.is_redirect is expected


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(
            Response(status_code=200, headers={"Content-Type": "text/html"}),
            "text/html",
            id="text/html",
        ),
        pytest.param(
            Response(
                status_code=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
            "application/json",
            id="application/json; charset=utf-8",
        ),
        pytest.param(Response(status_code=204), "", id="no content"),
    ],
)
def test_content_type(client: WebTestClient, response: Response, expected: str):
    wr = WebResponse(client, origin="", response=response)
    assert wr.content_type == expected


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(
            Response(
                status_code=200,
                headers={"Content-Type": "text/html", "Content-Length": "42"},
            ),
            {"Content-Type": "text/html", "Content-Length": "42"},
            id="text/html",
        ),
        pytest.param(Response(status_code=204), {}, id="no content"),
    ],
)
def test_headers(
    client: WebTestClient, response: Response, expected: Mapping[str, str]
):
    wr = WebResponse(client, origin="", response=response)
    assert wr.headers == expected


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(
            Response(
                status_code=200,
                content="hey",
                headers={"Content-Type": "text/plain"},
            ),
            "hey",
            id="content",
        ),
        pytest.param(Response(status_code=204), "", id="no content"),
    ],
)
def test_text(client: WebTestClient, response: Response, expected: str):
    wr = WebResponse(client, origin="", response=response)
    assert wr.text == expected


@pytest.mark.parametrize(
    "response,expected",
    [
        pytest.param(
            Response(
                status_code=200,
                content="<html><h1>hey</h1></html>",
            ),
            "hey",
            id="content",
        ),
        pytest.param(
            Response(
                status_code=204,
            ),
            "",
            id="no content",
        ),
    ],
)
def test_html(client: WebTestClient, response: Response, expected: str):
    wr = WebResponse(client, origin="", response=response)
    assert wr.html.text == expected


def test_html_body(client: WebTestClient):
    wr = WebResponse(
        client,
        origin="",
        response=Response(
            status_code=200,
            content="<html><body><h1>Hey</h1></body></html>",
        ),
    )
    assert wr.html_body.text == "Hey"


def test_html_nobody(client: WebTestClient):
    wr = WebResponse(client, origin="", response=Response(status_code=204))
    with pytest.raises(AssertionError) as ctx:
        wr.html_body  # noqa: B018
    assert str(ctx.value) == 'body element not found or multiple body found'


def test_html_form(client: WebTestClient):
    wr = WebResponse(
        client,
        origin="",
        response=Response(
            status_code=200,
            content="<html><body><form><input name='foo'></form></body></html>",
        ),
    )
    assert wr.form._formdata == {"foo": ""}  # type: ignore


@pytest.mark.parametrize(
    "response",
    [
        pytest.param(Response(status_code=204), id="nocontent"),
        pytest.param(
            Response(
                status_code=200,
                content="<html><body><h1>Hey</h1></body></html>",
            ),
            id="no form",
        ),
    ],
)
def test_form_none(client: WebTestClient, response: Response):
    wr = WebResponse(client, origin="", response=response)
    with pytest.raises(AssertionError) as ctx:
        wr.form  # noqa: B018
    assert str(ctx.value) == "form element not found"


def test_by_text(client: WebTestClient):
    wr = WebResponse(
        client,
        origin="",
        response=Response(
            status_code=200,
            content="<html><body><p id='here'>foo<p><b id='there'>foo<b></body></html>",
        ),
    )
    assert wr.by_text("foo").attrs["id"] == "here"  # type: ignore
    assert wr.by_text("foo", node_name="b").attrs["id"] == "there"  # type: ignore
    assert wr.by_text("bar") is None


def test_by_label_text(client: WebTestClient):
    wr = WebResponse(
        client,
        origin="",
        response=Response(
            status_code=200,
            content="""
                <form>
                    <label for="my-target">fetch target</label>
                    <input type="text" id="my-target">
                </form>
            """,
        ),
    )
    assert wr.by_label_text("fetch target").attrs["id"] == "my-target"  # type: ignore


def test_by_node_name(client: WebTestClient):
    wr = WebResponse(
        client,
        origin="",
        response=Response(
            status_code=200,
            content="""
                <form>
                    <label for="target=1">foo</label>
                    <input type="text" id="target-1">
                    <label for="target-2">bar</label>
                    <input type="text" id="target-2">
                </form>
            """,
        ),
    )
    nodes = wr.by_node_name("input")
    assert len(nodes) == 2
    assert nodes[0].attrs["id"] == "target-1"
    assert nodes[1].attrs["id"] == "target-2"
