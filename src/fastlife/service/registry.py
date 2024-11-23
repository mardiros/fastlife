from collections.abc import Mapping
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from fastlife.service.locale_negociator import LocaleNegociator  # coverage: ignore
    from fastlife.service.templates import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore
    from fastlife.service.translations import LocalizerFactory  # coverage: ignore

from fastlife.settings import Settings

TSettings = TypeVar("TSettings", bound=Settings, covariant=True)
"""
A TypeVar used to override the DefaultRegistry to add more helpers in the registry.
"""


class GenericRegistry(Generic[TSettings]):
    """
    Application registry for fastlife dependency injection.
    It is initialized by the configurator and accessed by the `fastlife.Registry`.
    """

    settings: Settings
    """Application settings."""
    renderers: Mapping[str, "AbstractTemplateRendererFactory"]
    """Registered template engine."""
    locale_negociator: "LocaleNegociator"
    """Used to fine the best language for the response."""
    localizer: "LocalizerFactory"
    """Used to localized message."""

    def __init__(self, settings: Settings) -> None:
        from fastlife.service.locale_negociator import default_negociator
        from fastlife.service.translations import LocalizerFactory

        self.settings = settings
        self.locale_negociator = default_negociator(self.settings)
        self.renderers = {}
        self.localizer = LocalizerFactory()

    def get_renderer(self, template: str) -> "AbstractTemplateRendererFactory":
        for key, val in self.renderers.items():
            if template.endswith(key):
                return val
        raise RuntimeError(f"No renderer registered for template {template}")


DefaultRegistry = GenericRegistry[Settings]
"""
The default registry until you need to inject more component in the registry.
"""


TRegistry = TypeVar("TRegistry", bound=DefaultRegistry, covariant=True)
"""
A TypeVar used to override the DefaultRegistry to add more helpers in the registry.
"""
