"""A dummy view to test the add_renderer"""

import json
from typing import Annotated

from fastapi import Path, Response

from fastlife import Localizer, TranslatableStringFactory, view_config

_ = TranslatableStringFactory(domain="fastlife_test")
lazy_dog = _("lazy dog")
quick_brown_fox = _("quick brown fox")


@view_config("more-i18n", "/{locale}/dummy-messages", methods=["GET"])
async def more_i18n(locale: Annotated[str, Path(...)], lczr: Localizer) -> Response:
    return Response(
        json.dumps(
            {
                "gettext": lczr.gettext(
                    "The {jumper} jumps over a {jumpee}",
                    jumper=lczr.gettext(quick_brown_fox),
                    jumpee=lczr.gettext(lazy_dog),
                ),
                "__call__": lczr(  # the same string is extracted
                    # but if you call the lczr gettext, it can handle it
                    # in a simpler way
                    "The {jumper} jumps over a {jumpee}",
                    jumper=lczr.gettext(quick_brown_fox),
                    jumpee=lczr.gettext(lazy_dog),
                ),
                "ngettext_0": lczr.ngettext(
                    "The quick brown fox jumps over a {jumpee}",
                    "{num} quick brown foxes jumps over a {jumpee}",
                    0,
                    jumpee=lczr.gettext(lazy_dog),
                ),
                "ngettext_1": lczr.ngettext(
                    "The quick brown fox jumps over a {jumpee}",
                    "{num} quick brown foxes jumps over a {jumpee}",
                    1,
                    jumpee=lczr.gettext(lazy_dog),
                ),
                "ngettext_2": lczr.ngettext(
                    "The quick brown fox jumps over a {jumpee}",
                    "{num} quick brown foxes jumps over a {jumpee}",
                    2,
                    jumpee=lczr.gettext(lazy_dog),
                ),
                "dgettext": lczr.dgettext(
                    "form_error",
                    "Invalid {field}",
                    field=lczr.gettext("email address"),
                ),
                "dngettext_0": lczr.dngettext(
                    "form_error",
                    "{num} entry in {field}",
                    "{num} entries in {field}",
                    0,
                    field=lczr.gettext("email address"),
                ),
                "dngettext_1": lczr.dngettext(
                    "form_error",
                    "{num} entry in {field}",
                    "{num} entries in {field}",
                    1,
                    field=lczr.gettext("email address"),
                ),
                "dngettext_2": lczr.dngettext(
                    "form_error",
                    "{num} entry in {field}",
                    "{num} entries in {field}",
                    2,
                    field=lczr.gettext("email address"),
                ),
                "pgettext_0": lczr.pgettext(
                    "verb_fish",
                    "fish",
                    unused=lczr.gettext("email address"),
                ),
                "pgettext_1": lczr.pgettext(
                    "noun_fish",
                    "fish",
                    unused=lczr.gettext("email address"),
                ),
                "dpgettext_1": lczr.dpgettext(
                    "form_error",
                    "label",
                    "{field} required",
                    field=lczr.gettext("email address"),
                ),
                "dpgettext_2": lczr.dpgettext(
                    "form_error",
                    "hint",
                    "{field} required",
                    field=lczr.gettext("email address"),
                ),
                "dnpgettext_0": lczr.dnpgettext(
                    "form_error",
                    "hint",
                    "{num} ball in {field}",
                    "{num} balls in {field}",
                    0,
                    field=lczr.gettext("email address"),
                ),
                "dnpgettext_1": lczr.dnpgettext(
                    "form_error",
                    "hint",
                    "{num} ball in {field}",
                    "{num} balls in {field}",
                    1,
                    field=lczr.gettext("email address"),
                ),
                "dnpgettext_2": lczr.dnpgettext(
                    "form_error",
                    "hint",
                    "{num} ball in {field}",
                    "{num} balls in {field}",
                    2,
                    field=lczr.gettext("email address"),
                ),
                "npgettext_0": lczr.npgettext(
                    "crayon",
                    "{} pen",
                    "{} pens",
                    0,
                ),
                "npgettext_1": lczr.npgettext(
                    "crayon",
                    "{} pen",
                    "{} pens",
                    1,
                ),
                "npgettext_2": lczr.npgettext(
                    "crayon",
                    "{} pen",
                    "{} pens",
                    2,
                ),
            }
        )
    )
