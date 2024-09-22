from pathlib import Path

import bs4
import pytest
from fastapi import Request as FastApiRequest

from fastlife import Request
from fastlife.config.registry import Registry
from fastlife.config.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer


@pytest.fixture(scope="session")
def components_dir() -> Path:
    return Path(__file__).parent / "components"


@pytest.fixture()
def settings(components_dir: Path) -> Settings:
    return Settings(template_search_path=f"{str(components_dir)},fastlife:components")


@pytest.fixture()
def dummy_request(dummy_registry: Registry) -> Request:
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
def renderer(settings: Settings, dummy_request: Request):
    return JinjaxTemplateRenderer(settings)(dummy_request)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
