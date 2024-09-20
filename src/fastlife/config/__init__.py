"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, configure
from .registry import AppRegistry, Registry
from .settings import Settings
from .views import view_config

__all__ = [
    "Configurator",
    "configure",
    "view_config",
    "Registry",
    "AppRegistry",
    "Settings",
]
