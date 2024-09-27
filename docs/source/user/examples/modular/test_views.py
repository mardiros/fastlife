import pytest
from entrypoint import app

from fastlife.testing import WebTestClient


@pytest.fixture
def client():
    return WebTestClient(app)


def test_views(client: WebTestClient):
    page = client.get("/")
    assert page.html.h1.text == "Hello world!"
