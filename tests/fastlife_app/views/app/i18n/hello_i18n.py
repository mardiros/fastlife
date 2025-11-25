"""A dummy view to test the i18n translations."""

from typing import Annotated

from fastapi import Path

from fastlife import Localizer, XTemplate, view_config
from fastlife.adapters.xcomponent.registry import x_component


@x_component()
def I18nHello(yolo: str, apple_count: int, orange_count: int, banana_count: int) -> str:
    return """<Layout>
        <H1>
            {globals.gettext("Hello, World!")}
        </H1>
        <p>
            {globals.gettext("How are you today ?")}
        </p>
        <p> {globals.gettext("Remember that {yolo}.", yolo=yolo)}</p>
        <p> {globals.ngettext("{num} apple", "{num} apples", apple_count)}</p>
        <p> {globals.ngettext("{num} orange", "{num} oranges", orange_count)}</p>
        <p> {globals.ngettext("banana!", "bananas!", banana_count)}</p>

        <A href={globals.request.url_path_for('more-i18n')}>{globals.gettext("See more...")}</A>
        </Layout>
    """


class HelloWorld(XTemplate):
    template = """<I18nHello
        yolo={yolo}
        apple_count={apple_count}
        orange_count={orange_count}
        banana_count={banana_count} />"""
    yolo: str
    apple_count: int
    orange_count: int
    banana_count: int


@view_config("hello-i18n", "/{locale}/hello", methods=["GET"])
async def hello_i18n(locale: Annotated[str, Path(...)], lczr: Localizer) -> HelloWorld:
    return HelloWorld(
        yolo=lczr.pgettext("Yolo", "you only live once"),
        apple_count=1,
        orange_count=2,
        banana_count=0,
    )
