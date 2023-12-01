import re
from typing import Any, Mapping

import pytest
from pydantic import BaseModel

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer
from fastlife.templating.renderer.widgets.base import Widget
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.dropdown import DropDownWidget
from fastlife.templating.renderer.widgets.sequence import SequenceWidget
from fastlife.templating.renderer.widgets.text import TextWidget
from fastlife.templating.renderer.widgets.union import UnionWidget


class Foo(BaseModel):
    name: str


class Bar(BaseModel):
    label: str


class Foobar(BaseModel):
    foobar: Foo | Bar


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "widget": TextWidget(
                    "name",
                    title="Name",
                    value="Robert Nesta",
                    aria_label="This is written on your ID card",
                    placeholder="John Doe",
                    help_text="This is written on your ID card",
                ),
                "expected_tags": [
                    {"tag": "label", "text": "Name"},
                    {
                        "tag": "input",
                        "attrs": {
                            "name": "name",
                            "type": "text",
                            "value": "Robert Nesta",
                            "placeholder": "John Doe",
                            "aria-label": "This is written on your ID card",
                        },
                    },
                    {
                        "tag": "span",
                        "text": "This is written on your ID card",
                    },
                ],
            },
            id="text",
        ),
        pytest.param(
            {
                "widget": TextWidget(
                    "name",
                    title="Name",
                    token="id",
                ),
                "expected_tags": [
                    {"tag": "label", "text": "Name", "for": "name-id"},
                    {
                        "tag": "input",
                        "attrs": {"id": "name-id", "name": "name"},
                    },
                ],
            },
            id="text",
        ),
        pytest.param(
            {
                "widget": TextWidget(
                    "email_address",
                    title="Email",
                    input_type="email",
                ),
                "expected_tags": [
                    {
                        "tag": "input",
                        "attrs": {"name": "email_address", "type": "email"},
                    },
                ],
            },
            id="email",
        ),
        pytest.param(
            {
                "widget": BooleanWidget(
                    "bared_foot",
                    title="Bared Foot",
                    token="id",
                ),
                "expected_tags": [
                    {"tag": "label", "text": "Bared Foot", "for": "bared-foot-id"},
                    {
                        "tag": "input",
                        "attrs": {"id": "bared-foot-id", "name": "bared_foot"},
                    },
                ],
            },
            id="text",
        ),
        pytest.param(
            {
                "widget": UnionWidget(
                    "foobar",
                    title="Foo Bar",
                    child=None,
                    children_types=[Foo, Bar],
                    token="abc",
                    removable=False,
                ),
                "expected_tags": [
                    {"tag": "button", "text": "Foo"},
                    {"tag": "button", "text": "Bar"},
                ],
            },
        ),
        pytest.param(
            {
                "widget": SequenceWidget(
                    "foobar",
                    title="Foo Bar",
                    help_text="",
                    item_type=str,
                    items=[
                        TextWidget(
                            "foobar.0",
                            title="Name",
                            token="id",
                        )
                    ],
                    token="abc",
                    removable=False,
                ),
                "expected_tags": [
                    {
                        "tag": "input",
                        "attrs": {"name": "foobar.0"},
                    },
                ],
            },
        ),
        pytest.param(
            {
                "widget": DropDownWidget(
                    "foobar",
                    title="Sides",
                    token="id",
                    options=["Rice", "Fries", "Salad"],
                    value="Salad",
                ),
                "expected_tags": [
                    {"tag": "label", "for": "side-id", "text": "Sides"},
                    {"tag": "select", "id": "side-id"},
                    {"tag": "option", "text": "Rice", "attrs": {"value": "Rice"}},
                    {"tag": "option", "text": "Fries", "attrs": {"value": "Fries"}},
                    {
                        "tag": "option",
                        "text": "Salad",
                        "attrs": {"value": "Salad", "selected": ""},
                    },
                ],
            },
        ),
    ],
)
async def test_widget(
    renderer: Jinja2TemplateRenderer, params: Mapping[str, Any], soup: Any
):
    widget: Widget = params["widget"]
    resp = await widget.to_html(renderer)
    html = soup(resp)
    for expected_tag in params["expected_tags"]:
        string = (
            re.compile(rf"\s*{expected_tag.get('text')}\s*")
            if "text" in expected_tag
            else None
        )
        tag = html.find(expected_tag["tag"], string=string)
        assert tag is not None, f"{expected_tag} in {resp}"
        for attr, val in expected_tag.get("attrs", {}).items():
            assert tag.attrs.get(attr) == val, attr
