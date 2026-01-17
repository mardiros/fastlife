from collections.abc import Callable

import bs4
from pydantic import BaseModel, Field

from fastlife import XTemplate
from fastlife.service.templates import AbstractTemplateRenderer


class Foo(BaseModel):
    name: str = Field(default="foo")


def test_pydantic_form_field(
    renderer: AbstractTemplateRenderer[XTemplate],
    soup: Callable[[str], bs4.BeautifulSoup],
):
    res = renderer.pydantic_form_field(
        Foo, name="f", token="x", removable=False, field=None
    )
    assert soup(res).find(
        "input",
        attrs={
            "id": "f-name-x",
            "name": "f.name",
            "type": "text",
            "value": "foo",
        },
    )
