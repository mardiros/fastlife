from importlib import metadata

__version__ = metadata.version("fastlifeweb")

from fastapi import Response
from fastapi.responses import RedirectResponse

from .adapters.fastapi.form import form_model
from .adapters.fastapi.localizer import Localizer
from .adapters.fastapi.request import (
    AnyRequest,
    Registry,
    Request,
    get_registry,
    get_request,
)
from .config import (
    Configurator,
    GenericConfigurator,
    configure,
    exception_handler,
    resource,
    resource_view,
    view_config,
)
from .domain.model.asgi import ASGIRequest, ASGIResponse
from .domain.model.form import FormModel
from .domain.model.request import GenericRequest
from .domain.model.security_policy import (
    Allowed,
    Anonymous,
    Authenticated,
    AuthenticationState,
    Denied,
    Forbidden,
    HasPermission,
    NoMFAAuthenticationState,
    PendingMFA,
    PreAuthenticated,
    TClaimedIdentity,
    TIdentity,
    Unauthenticated,
    Unauthorized,
)
from .domain.model.template import JinjaXTemplate

# from .request.form_data import model
from .service.registry import DefaultRegistry, GenericRegistry, TRegistry, TSettings
from .service.request_factory import RequestFactory
from .service.security_policy import (
    AbstractNoMFASecurityPolicy,
    AbstractSecurityPolicy,
    InsecurePolicy,
)
from .service.translations import TranslatableStringFactory
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
    "TSettings",
    "TRegistry",
    "get_registry",
    # Form
    "FormModel",
    "form_model",
    # Request
    "GenericRequest",
    "AnyRequest",
    "Request",
    "get_request",
    # Request Factory
    "ASGIRequest",
    "ASGIResponse",
    "RequestFactory",
    # Response
    "Response",
    "RedirectResponse",
    # Security
    "AbstractSecurityPolicy",
    "AbstractNoMFASecurityPolicy",
    "HasPermission",
    "Unauthenticated",
    "PreAuthenticated",
    "Allowed",
    "Denied",
    "Unauthorized",
    "Forbidden",
    "InsecurePolicy",
    "Anonymous",
    "PendingMFA",
    "Authenticated",
    "AuthenticationState",
    "NoMFAAuthenticationState",
    "TClaimedIdentity",
    "TIdentity",
    # Template
    "JinjaXTemplate",
    # i18n
    "Localizer",
    "TranslatableStringFactory",
]
