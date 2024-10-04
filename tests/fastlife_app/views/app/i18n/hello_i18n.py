"""A dummy view to test the i18n translations."""

from collections.abc import Mapping
from typing import Annotated, Any

from fastapi import Path

from fastlife import view_config
from fastlife.request.localizer import Localizer


@view_config(
    "hello-i18n", "/{locale}/hello", template="i18n.Hello.jinja", methods=["GET"]
)
async def hello_i18n(
    locale: Annotated[str, Path(...)], lczr: Localizer
) -> Mapping[str, Any]:
    return {
        "yolo": lczr.pgettext("Yolo", "you only live once"),
        "apple_count": 1,
        "orange_count": 2,
        "banana_count": 0,
    }
