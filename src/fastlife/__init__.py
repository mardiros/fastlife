from importlib import metadata

__version__ = metadata.version("fastlifeweb")

from fastapi import Response
from fastapi.responses import RedirectResponse

from .adapters.fastapi.form import form_model
from .adapters.fastapi.localizer import Localizer
from .adapters.fastapi.request import GenericRequest, Registry, Request, get_request
from .config import (
    Configurator,
    GenericConfigurator,
    configure,
    exception_handler,
    resource,
    resource_view,
    view_config,
)
from .domain.model.form import FormModel
from .domain.model.template import JinjaXTemplate

# from .request.form_data import model
from .services.registry import DefaultRegistry, GenericRegistry
from .settings import Settings

__all__ = [
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
    "exception_handler",
    # Model
    "Request",
    "GenericRequest",
    "get_request",
    "Registry",
    "Response",
    "RedirectResponse",
    # Form
    "form_model",
    "FormModel",
    # Template
    "JinjaXTemplate",
    # i18n
    "Localizer",
]
