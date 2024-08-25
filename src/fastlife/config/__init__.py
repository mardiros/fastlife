"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, configure
from .registry import AppRegistry, Registry

__all__ = [
    "Configurator",
    "configure",
    "Registry",
    "AppRegistry",
]
