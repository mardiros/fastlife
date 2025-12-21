"""A dummy view to test the add_renderer"""

from fastlife import view_config
from fastlife.domain.model.template import InlineTemplate
from tests.fastlife_app.adapters.fstring import FString


class HelloInline(FString):
    template = "Hello {name}!\n"
    name: str


@view_config("hello-inline-f-string", "/f-string", methods=["GET"])
async def hello_inline_fstring() -> InlineTemplate:
    return HelloInline(name="world")
