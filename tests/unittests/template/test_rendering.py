from pathlib import Path

import pytest
from fastapi import Request

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer, build_searchpath

template_path = str(Path(__file__).parent / "jinja2")


def test_build_searchpath(root_dir: Path):
    path_list = build_searchpath("fastlife:templates,/tmp")
    path = str(root_dir / "src" / "fastlife" / "templates")
    assert path_list == [path, "/tmp"]


async def test_jinja2_renderer():
    renderer = Jinja2TemplateRenderer(template_path)
    page = await renderer.render_template("hello_world.jinja2", title="say hello")
    assert "<title>say hello</title>" in page
    assert "<h1>Hello World!</h1>" in page


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "headers": [("cookie", "csrf_token=xxxCsrfTokenxxx")],
            }
        }
    ],
)
async def test_get_csrf_token(dummy_request_param: Request):
    renderer = Jinja2TemplateRenderer(template_path)
    page = await renderer.render_page(dummy_request_param, "csrf_token.jinja2")
    assert "xxxCsrfTokenxxx" in page
