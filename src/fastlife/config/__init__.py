"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, configure
from .registry import AppRegistry, Registry
from .settings import Settings

__all__ = [
    "Configurator",
    "configure",
    "Registry",
    "AppRegistry",
    "Settings",
]
