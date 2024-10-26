"""A dummy view to test the add_renderer"""

from collections.abc import Mapping
from typing import Any

from fastlife import view_config
from fastlife.templates import InlineTemplate


class HelloInline(InlineTemplate):
    template = "Hello {name}!\n"
    name: str


@view_config("hello-f-string", "/f-string", template="hello.fstring", methods=["GET"])
async def hello_fstring() -> Mapping[str, Any]:
    return {"name": "world"}


@view_config(
    "hello-inline-f-string", "/inline-f-string", template=".fstring", methods=["GET"]
)
async def hello_inline_fstring() -> InlineTemplate:
    return HelloInline(name="world")
