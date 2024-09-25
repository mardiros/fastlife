"""A dummy view to test the add_renderer"""

from typing import Annotated, Any, Mapping

from fastapi import Path, Response

from fastlife import view_config
from fastlife.request.localizer import Localizer


@view_config("hello-i18n", "/{locale}/dummy-messages", methods=["GET"])
async def hello_i18n(locale: Annotated[str, Path(...)], lczr: Localizer) -> Response:
    return Response(
        {
            "gettext": lczr.gettext(
                "The {jumper} jumps over a {jumpee}",
                mapping={
                    "jumper": lczr.gettext("quick brown fox"),
                    "jumpee": lczr.gettext("lazy dog"),
                },
            ),
            "ngettext": lczr.ngettext(
                "The quick brown fox jumps over a lazy dog",
                "The {jumper} jumps over a {jumpee}",
                1,
                mapping={
                    "jumper": lczr.gettext("quick brown fox"),
                    "jumpee": lczr.gettext("lazy dog"),
                },
            ),
        }
    )
