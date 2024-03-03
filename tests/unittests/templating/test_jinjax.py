from typing import Callable

import bs4

from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.dropdown import DropDownWidget
from fastlife.templating.renderer.widgets.hidden import HiddenWidget


async def test_render_template(renderer: JinjaxTemplateRenderer):
    res = await renderer.render_template("Page")
    assert (
        res
        == """\
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8" />
  <title>Fastlife</title>
</head>

<body><div>Hello World</div></body>

</html>\
"""
    )


async def test_render_boolean(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget("foo", title="Foo", token="XxX")
    result = await boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"}) is None


async def test_render_boolean_removable(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget("foo", title="Foo", token="XxX", removable=True)
    result = await boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"})


async def test_render_dropdown(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = DropDownWidget("foxo", title="Foo", options=["A", "B"], token="XxX")
    result = await boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foxo-XxX"})
    assert html.find("select", attrs={"id": "foxo-XxX", "name": "foxo"})


async def test_render_hidden(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = HiddenWidget("foo", value="bar", token="x")
    result = await hid.to_html(renderer)
    html = soup(result)
    assert html.find("input", attrs={"id": "foo-x", "name": "foo", "value": "bar"})
