"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, GenericConfigurator, configure
from .registry import DefaultRegistry, GenericRegistry
from .resources import resource, resource_view
from .settings import Settings
from .views import view_config

__all__ = [
    "Configurator",
    "GenericConfigurator",
    "configure",
    "view_config",
    "resource",
    "resource_view",
    "GenericRegistry",
    "DefaultRegistry",
    "Settings",
]
