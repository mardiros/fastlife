from collections.abc import Mapping
from typing import TYPE_CHECKING, Generic, TypeVar

from fastlife.services.locale_negociator import LocaleNegociator, default_negociator
from fastlife.services.translations import LocalizerFactory

if TYPE_CHECKING:
    from fastlife.services.templates import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore

from .settings import Settings

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
    renderers: Mapping[str, "AbstractTemplateRendererFactory"]
    locale_negociator: LocaleNegociator
    localizer: LocalizerFactory

    def __init__(self, settings: Settings) -> None:
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
