from pathlib import Path
from typing import Any, Callable, Mapping, Optional

import bs4
import pytest
from fastapi import Request
from pydantic import BaseModel, Field

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer, build_searchpath


class Person(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    admin: bool = Field(...)
    email: Optional[str] = Field(...)
    phone: str | None = Field(...)


def test_build_searchpath(root_dir: Path):
    path_list = build_searchpath("fastlife:templates,/tmp")
    path = str(root_dir / "src" / "fastlife" / "templates")
    assert path_list == [path, "/tmp"]


async def test_jinja2_renderer(renderer: Jinja2TemplateRenderer):
    page = await renderer.render_template("hello_world.jinja2", page_title="say hello")
    assert "<title>say hello</title>" in page
    assert "<h1>Hello World!</h1>" in page


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "headers": {"HX-Target": "body"},
            }
        }
    ],
)
async def test_hx_request(
    dummy_request_param: Request, renderer: Jinja2TemplateRenderer
):
    page = await renderer.render_page(dummy_request_param, "hello_world.jinja2")
    assert "<html>" not in page
    assert "<title>say hello</title>" not in page
    assert "<h1>Hello World!</h1>" in page


@pytest.mark.parametrize(
    "params",
    [{"request": {"csrf_token": "xxxCsrfTokenxxx"}}],
)
async def test_get_csrf_token(
    dummy_request_param: Request, renderer: Jinja2TemplateRenderer
):
    page = await renderer.render_page(dummy_request_param, "csrf_token.jinja2")
    assert "xxxCsrfTokenxxx" in page


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "request": {"headers": {"HX-Target": "body"}, "csrf_token": "xxx"},
                "kwargs": {"model": Person},
                "expected_inputs": {
                    "csrf_token": ("hidden", "xxx"),
                    "payload.admin": ("checkbox", "False"),
                    "payload.first_name": ("text", ""),
                    "payload.last_name": ("text", ""),
                    "payload.email": ("text", ""),
                    "payload.phone": ("text", ""),
                },
            },
            id="empty form",
        ),
        pytest.param(
            {
                "request": {"headers": {"HX-Target": "body"}, "csrf_token": "xxx"},
                "kwargs": {
                    "model": Person,
                    "form_data": {"payload": {"first_name": "Bob", "admin": True}},
                },
                "expected_inputs": {
                    "csrf_token": ("hidden", "xxx"),
                    "payload.admin": ("checkbox", "True"),
                    "payload.first_name": ("text", "Bob"),
                    "payload.last_name": ("text", ""),
                    "payload.email": ("text", ""),
                    "payload.phone": ("text", ""),
                },
            },
            id="load form data",
        ),
    ],
)
async def test_render_pydantic_form(
    params: Mapping[str, Any],
    dummy_request_param: Request,
    renderer: Jinja2TemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    page = await renderer.render_page(
        dummy_request_param, "pydantic_form.jinja2", **params["kwargs"]
    )
    html = soup(page)
    inputs = {
        tag["name"]: (tag["type"], tag["value"]) for tag in html.find_all("input")
    }
    assert inputs == params["expected_inputs"]
