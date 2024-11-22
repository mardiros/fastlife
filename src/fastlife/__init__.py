from importlib import metadata

__version__ = metadata.version("fastlifeweb")

from fastapi import Response
from fastapi.responses import RedirectResponse

from .config import (
    Configurator,
    GenericConfigurator,
    configure,
    resource,
    resource_view,
    view_config,
)
from .domain.model.template import JinjaXTemplate
from .request import GenericRequest, Registry, Request, get_request

# from .request.form_data import model

from .services.registry import DefaultRegistry, GenericRegistry
from .services.templates import TemplateParams
from .settings import Settings

__all__ = [
    # Config
    "configure",
    "GenericConfigurator",
    "Configurator",
    "DefaultRegistry",
    "GenericRegistry",
    "TemplateParams",
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
