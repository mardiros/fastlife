"""Settings for the fastlife."""

from datetime import timedelta
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings based on pydantic settings to configure the app.

    It can be overriden in order to inject application own settings.
    """

    model_config = SettingsConfigDict(env_prefix="fastlife_")
    """
    Set the prefix ``fastlife_`` for configuration using operating system environment.
    """

    fastlife_route_prefix: str = Field(default="/_fl")
    """Route prefix used for fastlife internal views."""
    template_search_path: str = Field(default="fastlife:components")
    """
    list of directories where components could be found by the template engine.

    the list is a comma separated string. The directory resolution is made from
    a python module name. for instance `fastlife:components` is the directory components
    found in the fastlife package.
    """
    registry_class: str = Field(default="fastlife.service.registry:DefaultRegistry")
    """Implementation class for the application regitry."""

    form_data_model_prefix: str = Field(default="payload")
    """
    Pydantic form default model prefix for serialized field in www-urlencoded-form.
    """
    csrf_token_name: str = Field(default="csrf_token")
    """
    Name of the html input field and for the http cookie for csrf token.
    """

    default_locale: str = Field(default="en")
    """
    The default locale
    """

    jinjax_file_ext: str = Field(default="jinja")
    """
    JinjaX file extention.
    """

    jinjax_use_cache: bool = Field(default=True)
    """
    JinjaX (the default template engine) setting use_cache.

    Could be disabled while developping, leave value true for production.
    """
    jinjax_auto_reload: bool = Field(default=False)
    """
    JinjaX (the default template engine) setting auto_reload.

    Set to true while developing, set false for production.
    """
    jinjax_global_catalog_class: str = Field(
        default="fastlife.template_globals:Globals"
    )
    """
    Set global constants accessible in every templates.
    Defaults to `fastlife.template_globals:Globals`
    See {class}`fastlife.template_globals.Globals`
    """

    session_secret_key: str = Field(default="")
    """
    A secret key, that could not changes for life.

    Used to securize the session with itsdangerous.
    """
    session_cookie_name: str = Field(default="flsess")
    """Cookie name for the session cookie."""
    session_cookie_domain: str = Field(default="")
    """Cookie domain for the session cookie."""
    session_cookie_path: str = Field(default="/")
    """Cookie path for the session cookie."""
    session_duration: timedelta = Field(default=timedelta(days=14))
    """Cookie duration for the session cookie."""
    session_cookie_same_site: Literal["lax", "strict", "none"] = Field(default="lax")
    """Cookie same-site for the session cookie."""
    session_cookie_secure: bool = Field(default=False)
    """
    Cookie secure for the session cookie,

    should be true while using https on production.
    """
    session_serializer: str = Field(
        default="fastlife.adapters.itsdangerous:SignedSessionSerializer"
    )
    """Cookie serializer for the session cookie."""

    domain_name: str = Field(default="", title="domain name where the app is served")
    """Domain name whre the app is served."""

    decode_reverse_proxy_headers: bool = Field(default=True)
    """Ensure that the request object has information based on http proxy headers."""
