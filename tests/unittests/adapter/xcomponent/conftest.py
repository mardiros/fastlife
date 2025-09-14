import bs4
import pytest
from fastapi import Request as FastApiRequest

from fastlife import Configurator, GenericRequest, Settings
from fastlife.adapters.xcomponent.renderer import XRendererFactory
from fastlife.service.templates import AbstractTemplateRenderer
from tests.fastlife_app.config import MyRegistry

Request = GenericRequest[MyRegistry, None, None]


@pytest.fixture
def conf(settings: Settings) -> Configurator:
    return Configurator(settings)


@pytest.fixture()
def dummy_request(dummy_registry: MyRegistry) -> Request:
    scope = {
        "type": "http",
        "headers": [("user-agent", "Mozilla/5.0"), ("accept", "text/html")],
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "path": "/",
    }
    req = Request(dummy_registry, FastApiRequest(scope))
    req.csrf_token.value = "CsRfT"
    return req


@pytest.fixture()
def x_renderer(settings: Settings):
    return XRendererFactory(settings)


@pytest.fixture()
async def renderer(
    conf: Configurator, x_renderer: XRendererFactory, dummy_request: Request
) -> AbstractTemplateRenderer:
    globs = await conf._build_renderer_globals(dummy_request)  # type: ignore
    ret = x_renderer(dummy_request)
    ret.globals.update(globs)
    return ret


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
