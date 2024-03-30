import bs4
import pytest
from anyio import Path
from fastapi import Request

from fastlife.configurator.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer

template_path = str(Path(__file__).parent / "components")


@pytest.fixture()
def dummy_request() -> Request:
    scope = {
        "type": "http",
        "headers": [("user-agent", "Mozilla/5.0"), ("accept", "text/html")],
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "path": "/",
    }
    req = Request(scope)
    return req


@pytest.fixture()
def renderer(dummy_request: Request):
    settings = Settings(template_search_path=f"{template_path},fastlife:templates")
    return JinjaxTemplateRenderer(settings)(dummy_request)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
