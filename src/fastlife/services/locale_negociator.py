"""Find the localization gor the given request."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from fastlife.config.settings import Settings

LocaleName = str
"""The LocaleName is a locale such as en, fr that will be consume for translations."""

if TYPE_CHECKING:
    from fastlife.request.request import GenericRequest  # coverage: ignore

    LocaleNegociator = Callable[[GenericRequest[Any]], LocaleName]  # coverage: ignore
    """Interface to implement to negociate a locale"""  # coverage: ignore
else:
    LocaleNegociator = Any


def default_negociator(settings: Settings) -> LocaleNegociator:
    """The default local negociator return the locale set in the conf."""

    def locale_negociator(request: "GenericRequest[Any]") -> str:
        return settings.default_locale

    return locale_negociator
