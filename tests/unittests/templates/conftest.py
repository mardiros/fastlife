from pathlib import Path

import bs4
import pytest
from fastapi import Request as FastApiRequest

from fastlife import Configurator, GenericRequest, Settings
from fastlife.adapters.jinjax import JinjaxEngine
from tests.fastlife_app.config import MyRegistry, MySettings

Request = GenericRequest[MyRegistry]


@pytest.fixture(scope="session")
def components_dir() -> Path:
    return Path(__file__).parent / "components"


@pytest.fixture()
def settings(components_dir: Path) -> MySettings:
    return MySettings(template_search_path=f"{components_dir!s},fastlife:components")


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
def jinjax_engine(settings: Settings):
    return JinjaxEngine(settings)


@pytest.fixture()
async def renderer(
    conf: Configurator, jinjax_engine: JinjaxEngine, dummy_request: Request
):
    globs = await conf._build_renderer_globals(dummy_request)  # type: ignore
    ret = jinjax_engine(dummy_request)
    ret.globals.update(globs)
    return ret


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
