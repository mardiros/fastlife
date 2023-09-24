from pathlib import Path

import bs4
import pytest

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer

template_path = str(Path(__file__).parent / "jinja2")


@pytest.fixture()
def renderer():
    return Jinja2TemplateRenderer(f"{template_path},fastlife:templates")


@pytest.fixture()
def soup():
    def bsoup(html: str):
        return bs4.BeautifulSoup(html, "html.parser")

    return bsoup
