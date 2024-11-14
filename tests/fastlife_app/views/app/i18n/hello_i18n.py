"""A dummy view to test the i18n translations."""

from typing import Annotated

from fastapi import Path

from fastlife import view_config
from fastlife.adapters.jinjax.inline import JinjaXTemplate
from fastlife.request.localizer import Localizer


class HelloWorld(JinjaXTemplate):
    template = """<i18n.Hello
        :yolo="yolo"
        :apple_count="apple_count"
        :orange_count="orange_count"
        :banana_count="banana_count" />"""
    yolo: str
    apple_count: int
    orange_count: int
    banana_count: int


@view_config(
    "hello-i18n", "/{locale}/hello", methods=["GET"]
)
async def hello_i18n(locale: Annotated[str, Path(...)], lczr: Localizer) -> HelloWorld:
    return HelloWorld(
        yolo=lczr.pgettext("Yolo", "you only live once"),
        apple_count=1,
        orange_count=2,
        banana_count=0,
    )
