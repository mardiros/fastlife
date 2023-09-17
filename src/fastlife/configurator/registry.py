from typing import Annotated

from fastapi import Depends

from fastlife.shared_utils.resolver import resolve
from fastlife.templating.renderer import AbstractTemplateRenderer

from .settings import Settings


class AppRegistry:
    renderer: AbstractTemplateRenderer

    def __init__(self, settings: Settings) -> None:
        TemplateRenderer = resolve(settings.template_renderer_class)
        self.renderer = TemplateRenderer(settings.template_search_path)


DEFAULT_REGISTRY: AppRegistry = None  # type: ignore


def initialize_registry(settings: Settings) -> None:
    global DEFAULT_REGISTRY
    if DEFAULT_REGISTRY is not None:
        raise ValueError("Registry is already set")
    AppRegistryCls = resolve(settings.registry_class)
    DEFAULT_REGISTRY = AppRegistryCls(settings)  # type: ignore


def cleanup_registry() -> None:
    """ "Method to cleanup the registry, used for testing"""
    global DEFAULT_REGISTRY
    DEFAULT_REGISTRY = None  # type: ignore


Registry = Annotated[AppRegistry, Depends(lambda: DEFAULT_REGISTRY)]
