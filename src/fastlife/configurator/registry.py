from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from fastlife.security.policy import CheckPermission
from fastlife.shared_utils.resolver import resolve

if TYPE_CHECKING:
    from fastlife.templating.renderer import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore

from .settings import Settings


class AppRegistry:
    settings: Settings
    renderer: "AbstractTemplateRendererFactory"
    check_permission: CheckPermission

    def __init__(self, settings: Settings) -> None:
        # Abtract class resolved for dependency injection
        TemplateRenderer = resolve(settings.template_renderer_class)

        self.settings = settings
        self.renderer = TemplateRenderer(settings)
        self.check_permission = resolve(settings.check_permission)


DEFAULT_REGISTRY: AppRegistry = None  # type: ignore


def initialize_registry(settings: Settings) -> AppRegistry:
    global DEFAULT_REGISTRY
    if DEFAULT_REGISTRY is not None:
        raise ValueError("Registry is already set")
    AppRegistryCls = resolve(settings.registry_class)
    DEFAULT_REGISTRY = AppRegistryCls(settings)  # type: ignore
    return DEFAULT_REGISTRY


def cleanup_registry() -> None:
    """ "Method to cleanup the registry, used for testing"""
    global DEFAULT_REGISTRY
    DEFAULT_REGISTRY = None  # type: ignore


Registry = Annotated[AppRegistry, Depends(lambda: DEFAULT_REGISTRY)]
