from typing import Any, Mapping

import pytest

from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer
from fastlife.templating.renderer.widgets.base import Widget
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.text import TextWidget


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
    ],
)
async def test_widget(
    renderer: Jinja2TemplateRenderer, params: Mapping[str, Any], soup: Any
):
    widget: Widget = params["widget"]
    resp = await widget.to_html(renderer)
    html = soup(resp)
    for expected_tag in params["expected_tags"]:
        tag = html.find(expected_tag["tag"])
        assert tag is not None, f"{expected_tag} in {resp}"
        for attr, val in expected_tag.get("attrs", {}).items():
            assert tag.attrs.get(attr) == val, tag.attrs
        if params.get("text"):
            assert tag.string == params["text"]
