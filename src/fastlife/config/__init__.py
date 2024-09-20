"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, configure
from .registry import AppRegistry, Registry
from .resources import resource, resource_view
from .settings import Settings
from .views import view_config

__all__ = [
    "Configurator",
    "configure",
    "view_config",
    "resource",
    "resource_view",
    "Registry",
    "AppRegistry",
    "Settings",
]
