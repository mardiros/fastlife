import bs4
import pytest
from anyio import Path

from fastlife.configurator.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer

template_path = str(Path(__file__).parent / "components")


@pytest.fixture()
def renderer():
    settings = Settings(
        template_search_path=f"{template_path},fastlife.templates:jinjax"
    )
    return JinjaxTemplateRenderer(settings)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
