from importlib import metadata

__version__ = metadata.version("fastlifeweb")

from fastapi import Response
from fastapi.responses import RedirectResponse

from .adapters.fastapi.form import form_model
from .adapters.fastapi.localizer import Localizer
from .adapters.fastapi.request import AnyRequest, Registry, Request, get_request
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
from .domain.model.request import GenericRequest
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
from .service.registry import DefaultRegistry, GenericRegistry
from .service.security_policy import AbstractSecurityPolicy, InsecurePolicy
from .settings import Settings

__all__ = [
    # Config
    "GenericConfigurator",
    "GenericRegistry",
    "Registry",
    "Settings",
    "configure",
    "view_config",
    "exception_handler",
    "resource",
    "resource_view",
    "Configurator",
    "DefaultRegistry",
    # Form
    "FormModel",
    "form_model",
    # Request
    "GenericRequest",
    "AnyRequest",
    "Request",
    "get_request",
    # Response
    "Response",
    "RedirectResponse",
    # Security
    "AbstractSecurityPolicy",
    "HasPermission",
    "Unauthenticated",
    "Allowed",
    "Denied",
    "Unauthorized",
    "Forbidden",
    "InsecurePolicy",
    # Template
    "JinjaXTemplate",
    # i18n
    "Localizer",
]
