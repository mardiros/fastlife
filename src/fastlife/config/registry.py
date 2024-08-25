from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from fastlife.config.route_handler import FastlifeRequest
from fastlife.security.policy import CheckPermission
from fastlife.shared_utils.resolver import resolve

if TYPE_CHECKING:
    from fastlife.templating.renderer import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore

from .settings import Settings


class AppRegistry:
    """
    The application registry got fastlife dependency injection.
    It is initialized by the configurator and accessed by the `fastlife.Registry`.
    """

    settings: Settings
    renderer: "AbstractTemplateRendererFactory"
    check_permission: CheckPermission

    def __init__(self, settings: Settings) -> None:
        # Abtract class resolved for dependency injection
        TemplateRenderer = resolve(settings.template_renderer_class)

        self.settings = settings
        self.renderer = TemplateRenderer(settings)
        self.check_permission = resolve(settings.check_permission)


def initialize_registry(settings: Settings) -> AppRegistry:
    # global DEFAULT_REGISTRY
    # if DEFAULT_REGISTRY is not None:  # type: ignore
    #     raise ValueError("Registry is already set")
    AppRegistryCls = resolve(settings.registry_class)
    return AppRegistryCls(settings)  # type: ignore


def get_registry(request: FastlifeRequest) -> AppRegistry:
    return request.registry


Registry = Annotated[AppRegistry, Depends(get_registry)]
"""FastAPI dependency to access to the registry."""
