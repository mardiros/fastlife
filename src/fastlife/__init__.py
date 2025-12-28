from importlib import metadata

__version__ = metadata.version("fastlifeweb")


from .adapters.fastapi.form import form_model
from .adapters.fastapi.localizer import Localizer
from .adapters.fastapi.request import (
    AnyRequest,
    Registry,
    Request,
    get_registry,
    get_request,
)
from .adapters.fastapi.websocket import GenericWebSocket, WebSocket
from .adapters.xcomponent.pydantic_form.widgets.base import CustomWidget, Widget
from .adapters.xcomponent.pydantic_form.widgets.boolean import BooleanWidget
from .adapters.xcomponent.pydantic_form.widgets.checklist import ChecklistWidget
from .adapters.xcomponent.pydantic_form.widgets.dropdown import (
    DropDownWidget,
    DropDownWidgetOption,
)
from .adapters.xcomponent.pydantic_form.widgets.hidden import HiddenWidget
from .adapters.xcomponent.pydantic_form.widgets.mfa_code import MFACodeWidget
from .adapters.xcomponent.pydantic_form.widgets.model import ModelWidget
from .adapters.xcomponent.pydantic_form.widgets.sequence import SequenceWidget
from .adapters.xcomponent.pydantic_form.widgets.text import (
    PasswordWidget,
    TextareaWidget,
    TextWidget,
)
from .adapters.xcomponent.pydantic_form.widgets.union import UnionWidget
from .adapters.xcomponent.registry import x_component, x_function
from .config import (
    Configurator,
    GenericConfigurator,
    configure,
    exception_handler,
    resource,
    resource_view,
    scheduled_job,
    view_config,
    websocket_view,
)
from .domain.model.asgi import ASGIRequest, ASGIResponse
from .domain.model.form import FormModel
from .domain.model.request import GenericRequest
from .domain.model.response import RedirectResponse, Response
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
from .domain.model.template import XTemplate

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
    "websocket_view",
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
    # Websockets
    "GenericWebSocket",
    "WebSocket",
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
    "XTemplate",
    "x_component",
    "x_function",
    # Widgets
    "CustomWidget",
    "Widget",
    "BooleanWidget",
    "ChecklistWidget",
    "DropDownWidget",
    "DropDownWidgetOption",
    "HiddenWidget",
    "MFACodeWidget",
    "ModelWidget",
    "SequenceWidget",
    "TextWidget",
    "PasswordWidget",
    "TextareaWidget",
    "UnionWidget",
    # i18n
    "Localizer",
    "TranslatableStringFactory",
    # scheduled jobs
    "scheduled_job",
]
