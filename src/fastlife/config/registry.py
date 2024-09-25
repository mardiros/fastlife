from collections.abc import Mapping
from typing import TYPE_CHECKING, Annotated, Callable

from fastapi import Depends
from fastapi import Request as FastAPIRequest

from fastlife.request.request import Request
from fastlife.security.policy import CheckPermission
from fastlife.services.translations import LocalizerFactory
from fastlife.shared_utils.resolver import resolve

if TYPE_CHECKING:
    from fastlife.services.templates import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore

from .settings import Settings

LocaleNegociator = Callable[[Request], str]


def _default_negociator(settings: Settings) -> LocaleNegociator:
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
    check_permission: CheckPermission
    locale_negociator: LocaleNegociator
    localizer: LocalizerFactory

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.check_permission = resolve(settings.check_permission)
        self.locale_negociator = _default_negociator(self.settings)
        self.renderers = {
            f".{settings.jinjax_file_ext}": resolve(
                "fastlife.adapters.jinjax.renderer:JinjaxTemplateRenderer"
            )(settings),
        }
        self.localizer = LocalizerFactory()

    def get_renderer(self, template: str) -> "AbstractTemplateRendererFactory":
        for key, val in self.renderers.items():
            if template.endswith(key):
                return val
        raise RuntimeError(f"No renderer registered for template {template}")


def get_registry(request: Request) -> AppRegistry:
    return request.registry


Registry = Annotated[AppRegistry, Depends(get_registry)]
"""FastAPI dependency to access to the registry."""
