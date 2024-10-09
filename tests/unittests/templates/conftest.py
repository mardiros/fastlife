from pathlib import Path

import bs4
import pytest
from fastapi import Request as FastApiRequest

from fastlife import GenericRequest, Settings
from fastlife.adapters.jinjax import JinjaxTemplateRenderer
from tests.fastlife_app.config import MyRegistry, MySettings

Request = GenericRequest[MyRegistry]


@pytest.fixture(scope="session")
def components_dir() -> Path:
    return Path(__file__).parent / "components"


@pytest.fixture()
def settings(components_dir: Path) -> MySettings:
    return MySettings(template_search_path=f"{components_dir!s},fastlife:components")


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
    return req


@pytest.fixture()
def jinjax_engine(settings: Settings):
    return JinjaxTemplateRenderer(settings)


@pytest.fixture()
def renderer(jinjax_template_engine: JinjaxTemplateRenderer, dummy_request: Request):
    return jinjax_template_engine(dummy_request)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
