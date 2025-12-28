"""Configure fastlife app for dependency injection."""

from .configurator import Configurator, GenericConfigurator, configure
from .exceptions import exception_handler
from .jobs import scheduled_job
from .resources import resource, resource_view
from .views import view_config
from .websockets import websocket_view

__all__ = [
    "Configurator",
    "GenericConfigurator",
    "configure",
    "exception_handler",
    "scheduled_job",
    "resource",
    "resource_view",
    "view_config",
    "websocket_view",
]
