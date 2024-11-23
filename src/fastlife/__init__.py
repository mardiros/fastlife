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
from .domain.model.security_policy import (
    Allowed,
    Denied,
    Forbidden,
    HasPermission,
    Unauthenticated,
    Unauthorized,
)
from .domain.model.template import JinjaXTemplate

# from .request.form_data import model
from .services.registry import DefaultRegistry, GenericRegistry
from .services.security_policy import AbstractSecurityPolicy, InsecurePolicy
from .settings import Settings

__all__ = [
    "AbstractSecurityPolicy",
    # Security policy
    "Allowed",
    "Configurator",
    "DefaultRegistry",
    "Denied",
    "Forbidden",
    "FormModel",
    "GenericConfigurator",
    "GenericRegistry",
    "GenericRequest",
    "HasPermission",
    "InsecurePolicy",
    # Template
    "JinjaXTemplate",
    # i18n
    "Localizer",
    "RedirectResponse",
    "Registry",
    # Model
    "Request",
    "Response",
    "Settings",
    "Unauthenticated",
    "Unauthorized",
    # Config
    "configure",
    "exception_handler",
    # Form
    "form_model",
    "get_request",
    "resource",
    "resource_view",
    "view_config",
]
