from pathlib import Path

import bs4
import pytest
from fastapi import Request

from fastlife.configurator.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer


@pytest.fixture(scope="session")
def components_dir() -> Path:
    return Path(__file__).parent / "components"


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
def renderer(dummy_request: Request, components_dir: Path):
    settings = Settings(
        template_search_path=f"{str(components_dir)},fastlife:templates"
    )
    return JinjaxTemplateRenderer(settings)(dummy_request)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
