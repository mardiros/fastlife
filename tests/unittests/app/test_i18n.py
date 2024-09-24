import pytest

from fastlife.testing import WebTestClient


def test_http_call(client: WebTestClient):
    resp = client.get("/fr/hello")
    assert resp.html.h1.text == "Salut tout le monde !"
