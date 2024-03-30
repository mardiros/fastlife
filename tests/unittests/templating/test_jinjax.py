from typing import Callable

import bs4
from pydantic import BaseModel

from fastlife.templating.renderer.jinjax import AbstractTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.dropdown import DropDownWidget
from fastlife.templating.renderer.widgets.hidden import HiddenWidget
from fastlife.templating.renderer.widgets.model import ModelWidget
from fastlife.templating.renderer.widgets.sequence import SequenceWidget
from fastlife.templating.renderer.widgets.text import TextWidget
from fastlife.templating.renderer.widgets.union import UnionWidget


def test_render_template(renderer: AbstractTemplateRenderer):
    res = renderer.render_template("Page")
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


def test_render_boolean(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget("foo", title="Foo", token="XxX")
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"}) is None


def test_render_boolean_removable(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget("foo", title="Foo", token="XxX", removable=True)
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"})


def test_render_dropdown(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = DropDownWidget("foxo", title="Foo", options=["A", "B"], token="XxX")
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foxo-XxX"})
    assert html.find("select", attrs={"id": "foxo-XxX", "name": "foxo"})


def test_render_hidden(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = HiddenWidget("foo", value="bar", token="x")
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "hidden", "name": "foo", "value": "bar"}
    )


def test_render_text(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget("foo", title="Foo", value="bar", token="x")
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )


def test_render_text_help(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget(
        "foo", title="Foo", value="bar", token="x", help_text="This is foobar"
    )
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )
    help_text = html.find("span")
    assert help_text
    assert help_text.text == "This is foobar"


def test_render_text_removable(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    text = TextWidget("foo", title="Foo", token="x", removable=True)
    result = text.to_html(renderer)
    html = soup(result)
    assert html.find("button", attrs={"type": "button"})


def test_render_model(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = ModelWidget(
        "foo",
        title="Foo",
        children_widget=[TextWidget("name", title="n", token="x", removable=True)],
        removable=False,
        token="x",
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "name-x", "type": "text"})


def test_render_sequence(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
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
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("details", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "x-x", "type": "text"})
    assert html.find("input", attrs={"id": "y-x", "type": "text"})


def test_render_union(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    class Foo(BaseModel):
        foo: str

    class Bar(BaseModel):
        bar: str

    model = UnionWidget(
        "foobar",
        title="foobar",
        child=None,
        children_types=[Foo, Bar],
        removable=False,
        token="x",
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foobar-x"})

    # assert html.find("button", attrs={})
