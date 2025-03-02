from collections.abc import Callable, Mapping, Sequence
from typing import Any

import bs4
import pytest
from pydantic import BaseModel

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.boolean import BooleanWidget
from fastlife.adapters.jinjax.widgets.checklist import Checkable, ChecklistWidget
from fastlife.adapters.jinjax.widgets.dropdown import DropDownWidget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget
from fastlife.adapters.jinjax.widgets.mfa_code import MFACodeWidget
from fastlife.adapters.jinjax.widgets.model import ModelWidget
from fastlife.adapters.jinjax.widgets.sequence import SequenceWidget
from fastlife.adapters.jinjax.widgets.text import TextareaWidget, TextWidget
from fastlife.adapters.jinjax.widgets.union import UnionWidget
from fastlife.domain.model.types import Builtins
from fastlife.service.templates import AbstractTemplateRenderer


class Foo(BaseModel): ...


def test_render_boolean(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget(name="foo", title="Foo", token="XxX")
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"}) is None


def test_render_boolean_removable(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    boolean = BooleanWidget(name="foo", title="Foo", token="XxX", removable=True)
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foo-XxX"})
    assert html.find("input", attrs={"id": "foo-XxX", "name": "foo"})
    assert html.find("button", attrs={"type": "button"})


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {"options": None, "expected_text": [], "expected_value": []},
            id="None",
        ),
        pytest.param(
            {
                "options": ["A", "B"],
                "expected_text": ["A", "B"],
                "expected_value": ["A", "B"],
            },
            id="list[str]",
        ),
        pytest.param(
            {
                "options": [("A", "A Plan"), ("B", "B Plan")],
                "expected_text": ["A Plan", "B Plan"],
                "expected_value": ["A", "B"],
            },
            id="list[tuple[str,str]]",
        ),
    ],
)
def test_render_dropdown(
    params: Mapping[str, Any],
    renderer: AbstractTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    boolean = DropDownWidget(
        name="foxo", title="Foo", options=params["options"], token="XxX"
    )
    result = boolean.to_html(renderer)
    html = soup(result)
    assert html.find("label", attrs={"for": "foxo-XxX"})

    select = html.find("select", attrs={"id": "foxo-XxX", "name": "foxo"})
    assert isinstance(select, bs4.Tag)
    assert [n.attrs["value"] for n in select.find_all("option")] == params[
        "expected_value"
    ]
    assert [n.text for n in select.find_all("option")] == params["expected_text"]


def test_render_hidden(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = HiddenWidget(name="foo", value="bar", token="x")
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "hidden", "name": "foo", "value": "bar"}
    )


def test_render_text(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget(name="foo", title="Foo", value="bar", token="x")
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )


def test_render_text_help(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    hid = TextWidget(
        name="foo", title="Foo", value="bar", token="x", hint="This is foobar"
    )
    result = hid.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input", attrs={"id": "foo-x", "type": "text", "name": "foo", "value": "bar"}
    )
    hint = html.find("span")
    assert hint
    assert hint.text == "This is foobar"


def test_render_text_removable(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    text = TextWidget(name="foo", title="Foo", token="x", removable=True)
    result = text.to_html(renderer)
    html = soup(result)
    assert html.find("button", attrs={"type": "button"})


def test_render_mfa_code(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    text = MFACodeWidget(name="foo", title="Foo", token="x", hint="This is foobar")
    result = text.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "foo-x",
            "type": "text",
            "name": "foo",
            "inputmode": "numeric",
            "autocomplete": "one-time-code",
            "autofocus": True,
        },
    )
    hint = html.find("span")
    assert hint
    assert hint.text == "This is foobar"


def test_render_mfa_code_no_focus(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    text = MFACodeWidget(name="foo", title="Foo", token="x", autofocus=False)
    result = text.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "foo-x",
            "type": "text",
            "name": "foo",
            "inputmode": "numeric",
            "autocomplete": "one-time-code",
        },
    )


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("foobar", "foobar", id="str"),
        pytest.param(["foo", "bar"], "foo\nbar", id="sequence"),
    ],
)
def test_render_textarea(
    renderer: AbstractTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
    value: str | Sequence[str],
    expected: str,
):
    hid = TextareaWidget(name="foo", title="Foo", value=["foo", "bar"], token="x")
    result = hid.to_html(renderer)
    html = soup(result)
    textarea = html.find("textarea", attrs={"id": "foo-x", "name": "foo"})
    assert textarea
    assert textarea.text == "foo\nbar"


def test_render_model(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = ModelWidget[TextWidget](
        name="foo",
        title="Foo",
        value=[TextWidget(name="name", title="n", token="x", removable=True)],
        removable=False,
        token="x",
        nested=False,
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "name-x", "type": "text"})


def test_render_nested_model(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = ModelWidget[Widget[Builtins]](
        name="foo",
        title="Foo",
        value=[TextWidget(name="name", title="n", token="x", removable=True)],
        removable=False,
        token="x",
        nested=True,
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foo-x"})
    assert html.find("summary", attrs={"id": "foo-x-summary"})
    assert html.find("input", attrs={"id": "name-x", "type": "text"})


def test_render_sequence(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = SequenceWidget[TextWidget](
        name="foo",
        title="Foo",
        value=[
            TextWidget(name="x", title="x", token="x", removable=True),
            TextWidget(name="y", title="y", token="x", removable=True),
        ],
        removable=False,
        token="x",
        hint="",
        item_type=str,
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("details", attrs={"id": "foo-x"})
    assert html.find("input", attrs={"id": "x-x", "type": "text"})
    assert html.find("input", attrs={"id": "y-x", "type": "text"})


def test_render_checklist(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    model = ChecklistWidget(
        name="foobar",
        title="Foobar",
        value=[
            Checkable(label="Foo", name="foobar", value="f", token="x", checked=True),
            Checkable(label="Bar", name="foobar", value="b", token="x", checked=False),
            Checkable(label="Baz", name="foobar", value="z", token="x", checked=False),
        ],
        token="x",
        removable=False,
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find(
        "input",
        attrs={"id": "foobar-f-x", "type": "checkbox", "value": "f", "checked": True},
    )
    lbl = html.find("label", attrs={"for": "foobar-f-x"})
    assert isinstance(lbl, bs4.Tag)
    assert lbl.text.strip() == "Foo"
    b = html.find("input", attrs={"id": "foobar-b-x", "type": "checkbox", "value": "b"})
    assert isinstance(b, bs4.Tag)
    assert "checked" not in b.attrs
    assert html.find(
        "input", attrs={"id": "foobar-z-x", "type": "checkbox", "value": "z"}
    )


def test_render_union(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    class Foo(BaseModel):
        foo: str

    class Bar(BaseModel):
        bar: str

    model = UnionWidget[Any](
        name="foobar",
        title="foobar",
        value=None,
        children_types=[Foo, Bar],
        removable=False,
        token="x",
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foobar-x"})


def test_render_custom(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    class CustomWidget(Widget[Any]):
        template = """
        <div id="{{id}}" contenteditable>{{value}}</div>
        {% if error %}
        <p id="{{id}}-error">{{error}}</p>
        {% endif %}
        """

    model = CustomWidget(
        name="foo",
        title="foo",
        value="foobar",
        removable=False,
        token="x",
    )
    result = model.to_html(renderer)
    html = soup(result)
    assert html.find("div", attrs={"id": "foo-x", "contenteditable": True})


@pytest.mark.parametrize(
    "widget",
    [
        pytest.param(
            TextWidget(name="foo", title="Foo", token="x", error="It did not work"),
            id="text",
        ),
        pytest.param(
            BooleanWidget(name="foo", title="Foo", token="x", error="It did not work"),
            id="boolean",
        ),
        pytest.param(
            DropDownWidget(
                name="foo",
                title="Foo",
                options=["A"],  # type: ignore
                token="x",
                error="It did not work",
            ),
            id="dropdown",
        ),
        pytest.param(
            ChecklistWidget(
                name="foo",
                title="Foobar",
                value=[
                    Checkable(
                        label="Foo", name="foobar", value="f", token="x", checked=True
                    ),
                ],
                token="x",
                removable=False,
                error="It did not work",
            ),
            id="checklist",
        ),
        pytest.param(
            ChecklistWidget(
                name="foo",
                title="Foobar",
                value=[
                    Checkable(
                        label="Foo",
                        name="foobar",
                        value="f",
                        token="x",
                        checked=True,
                        error="It did not work",
                    ),
                ],
                token="x",
                removable=False,
            ),
            id="checklist-checkable",
        ),
        pytest.param(
            SequenceWidget[TextWidget](
                name="foo",
                title="Foo",
                value=[
                    TextWidget(name="x", title="x", token="x", removable=True),
                ],
                removable=False,
                token="x",
                hint="",
                item_type=str,
                error="It did not work",
            ),
            id="sequence",
        ),
        pytest.param(
            UnionWidget[Any](
                name="foo",
                title="foo",
                value=None,
                error="It did not work",
                children_types=[Foo],
                removable=False,
                token="x",
            ),
            id="union",
        ),
        pytest.param(
            ModelWidget[TextWidget](
                name="foo",
                title="Foo",
                value=[TextWidget(name="name", title="n", token="x", removable=True)],
                error="It did not work",
                removable=False,
                token="x",
                nested=True,
            ),
            id="model-widget",
        ),
    ],
)
def test_render_text_error(
    renderer: AbstractTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
    widget: Widget[Any],
):
    result = widget.to_html(renderer)
    html = soup(result)
    assert html.find(string="It did not work")
