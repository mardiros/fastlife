"""A dummy view to test the add_renderer"""

from fastlife import view_config
from fastlife.templates import InlineTemplate


class HelloInline(InlineTemplate):
    template = "Hello {name}!\n"
    renderer = ".fstring"
    name: str


@view_config("hello-inline-f-string", "/f-string", template=".fstring", methods=["GET"])
async def hello_inline_fstring() -> InlineTemplate:
    return HelloInline(name="world")
