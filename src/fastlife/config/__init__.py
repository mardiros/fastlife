"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, GenericConfigurator, configure
from .exceptions import exception_handler
from .resources import resource, resource_view
from .views import view_config

__all__ = [
    "Configurator",
    "GenericConfigurator",
    "configure",
    "view_config",
    "resource",
    "resource_view",
    "exception_handler",
]
