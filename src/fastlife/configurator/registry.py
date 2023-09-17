from typing import Annotated

from fastapi import Depends

from fastlife.templating.renderer import AbstractTemplateRenderer
from fastlife.templating.renderer.jinja2 import Jinja2TemplateRenderer

from .settings import Settings


class AppRegistry:
    renderer: AbstractTemplateRenderer

    def __init__(self, settings: Settings) -> None:
        self.renderer = Jinja2TemplateRenderer(settings.template_search_path)


DEFAULT_REGISTRY: AppRegistry = None  # type: ignore


def initialize_registry(settings: Settings) -> None:
    global DEFAULT_REGISTRY
    if DEFAULT_REGISTRY is not None:
        raise ValueError("Registry is already set")
    DEFAULT_REGISTRY = AppRegistry(settings)  # type: ignore


def cleanup_registry() -> None:
    """ "Method to cleanup the registry, used for testing"""
    global DEFAULT_REGISTRY
    DEFAULT_REGISTRY = None  # type: ignore


Registry = Annotated[AppRegistry, Depends(lambda: DEFAULT_REGISTRY)]
