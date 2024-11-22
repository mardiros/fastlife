from importlib import metadata

__version__ = metadata.version("fastlifeweb")

from fastapi import Response
from fastapi.responses import RedirectResponse

from .adapters.fastapi.form import form_model
from .adapters.fastapi.request import GenericRequest, Registry, Request, get_request
from .config import (
    Configurator,
    GenericConfigurator,
    configure,
    resource,
    resource_view,
    view_config,
)
from .domain.model.template import JinjaXTemplate

# from .request.form_data import model
from .services.registry import DefaultRegistry, GenericRegistry
from .settings import Settings

__all__ = [
    "form_model",
    # Config
    "configure",
    "GenericConfigurator",
    "Configurator",
    "DefaultRegistry",
    "GenericRegistry",
    "Settings",
    "view_config",
    "resource",
    "resource_view",
    # Model
    # "model",
    "Request",
    "GenericRequest",
    "get_request",
    "Registry",
    "Response",
    "RedirectResponse",
    # Template
    "JinjaXTemplate",
]
