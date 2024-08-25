from starlette.types import ASGIApp

from fastlife.config.settings import Settings
from fastlife.testing.testclient import WebTestClient


def test_default(app: ASGIApp):
    client = WebTestClient(app)
    assert client.settings.domain_name == "testserver.local"
    assert client.session == {}


def test_init_from_setting(app: ASGIApp):
    client = WebTestClient(app, settings=Settings(domain_name="yolo.local"))
    assert client.settings.domain_name == "yolo.local"
