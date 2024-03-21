from typing import Callable

import bs4

from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.dropdown import DropDownWidget
from fastlife.templating.renderer.widgets.hidden import HiddenWidget
from fastlife.templating.renderer.widgets.model import ModelWidget
from fastlife.templating.renderer.widgets.sequence import SequenceWidget
from fastlife.templating.renderer.widgets.text import TextWidget


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
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "hidden", "name": "foo", "value": "bar"}
    )


async def test_render_text(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget("foo", title="Foo", value="bar", token="x")
    result = await hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )


async def test_render_text_help(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget(
        "foo", title="Foo", value="bar", token="x", help_text="This is foobar"
    )
    result = await hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )
    help_text = html.find("span")
    assert help_text
    assert help_text.text == "This is foobar"


async def test_render_text_removable(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    text = TextWidget("foo", title="Foo", token="x", removable=True)
    result = await text.to_html(renderer)
    html = soup(result)
    assert html.find("button", attrs={"type": "button"})


async def test_render_model(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = ModelWidget(
        "foo",
        title="Foo",
        children_widget=[TextWidget("name", title="n", token="x", removable=True)],
        removable=False,
        token="x",
    )
    result = await model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "name-x", "type": "text"})


async def test_render_sequence(
    renderer: JinjaxTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = SequenceWidget(
        "foo",
        title="Foo",
        items=[
            TextWidget("x", title="x", token="x", removable=True),
            TextWidget("y", title="y", token="x", removable=True),
        ],
        removable=False,
        token="x",
        help_text="",
        item_type=str,
    )
    result = await model.to_html(renderer)
    html = soup(result)
    assert html.find("details", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "x-x", "type": "text"})
    assert html.find("input", attrs={"id": "y-x", "type": "text"})
