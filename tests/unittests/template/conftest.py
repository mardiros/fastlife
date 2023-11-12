from pathlib import Path

import bs4
import pytest

from fastlife.configurator.settings import Settings
from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer

template_path = str(Path(__file__).parent / "jinja2")


@pytest.fixture()
def renderer():
    settings = Settings(template_search_path=f"{template_path},fastlife:templates")
    return Jinja2TemplateRenderer(settings)


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
