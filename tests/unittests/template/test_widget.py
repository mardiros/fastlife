import re
from typing import Any, Mapping

import pytest
from pydantic import BaseModel

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer
from fastlife.templating.renderer.widgets.base import Widget
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.text import TextWidget
from fastlife.templating.renderer.widgets.union import TypeWrapper, UnionWidget


class Foo(BaseModel):
    name: str


class Bar(BaseModel):
    label: str


def test_typewrapper():
    tw = TypeWrapper(Foo, route_prefix="/_")
    assert tw.fullname == "tests.unittests.template.test_widget:Foo"
    assert (
        tw.get_url("placeholder") == "/_/pydantic-form/widgets/"
        "tests.unittests.template.test_widget:Foo?name=placeholder"
    )


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "widget": TextWidget(
                    "name",
                    title="Name",
                    value="Robert Nesta",
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
                    id="name-id",
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
                    id="bared-foot-id",
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
                    "foobar", title="Foo Bar", child=None, children_types=[Foo, Bar]
                ),
                "expected_tags": [
                    {"tag": "button", "text": "Foo"},
                    {"tag": "button", "text": "Bar"},
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
            assert tag.attrs.get(attr) == val, tag.attrs
