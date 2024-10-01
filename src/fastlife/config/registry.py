from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from fastapi import Request as FastAPIRequest

from fastlife.services.translations import LocalizerFactory

if TYPE_CHECKING:
    from fastlife.request.request import GenericRequest
    from fastlife.services.templates import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore

from .settings import Settings


def _default_negociator(settings: Settings) -> "Callable[[GenericRequest[Any]], str]":
    def locale_negociator(request: FastAPIRequest) -> str:
        return settings.default_locale

    return locale_negociator


class AppRegistry:
    """
    The application registry got fastlife dependency injection.
    It is initialized by the configurator and accessed by the `fastlife.Registry`.
    """

    settings: Settings
    renderers: Mapping[str, "AbstractTemplateRendererFactory"]
    locale_negociator: "Callable[[GenericRequest[Any]], str]"
    localizer: LocalizerFactory

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.locale_negociator = _default_negociator(self.settings)
        self.renderers = {}
        self.localizer = LocalizerFactory()

    def get_renderer(self, template: str) -> "AbstractTemplateRendererFactory":
        for key, val in self.renderers.items():
            if template.endswith(key):
                return val
        raise RuntimeError(f"No renderer registered for template {template}")


TRegistry = TypeVar("TRegistry", bound=AppRegistry)
