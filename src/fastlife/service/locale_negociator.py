"""Find the localization gor the given request."""

from collections.abc import Callable
from typing import Any

from fastlife.settings import Settings

LocaleName = str
"""The LocaleName is a locale such as en, fr that will be consume for translations."""

from fastlife.adapters.fastapi.request import GenericRequest

LocaleNegociator = Callable[[GenericRequest[Any, Any, Any]], LocaleName]
"""Interface to implement to negociate a locale"""


def default_negociator(settings: Settings) -> LocaleNegociator:
    """The default local negociator return the locale set in the conf."""

    def locale_negociator(request: "GenericRequest[Any, Any, Any]") -> str:
        return settings.default_locale

    return locale_negociator
