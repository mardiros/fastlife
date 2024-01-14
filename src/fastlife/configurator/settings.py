from datetime import timedelta
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="fastlife_")

    fastlife_route_prefix: str = Field(default="/_fl")
    template_search_path: str = Field(default="fastlife:templates")
    registry_class: str = Field(default="fastlife.configurator.registry:AppRegistry")
    template_renderer_class: str = Field(
        default="fastlife.templating.renderer.jinja2:Jinja2TemplateRenderer"
    )
    form_data_model_prefix: str = Field(default="payload")
    csrf_token_name: str = Field(default="csrf_token")

    session_secret_key: str = Field(default="")
    session_cookie_name: str = Field(default="flsess")
    session_cookie_path: str = Field(default="/")
    session_duration: timedelta = Field(default=timedelta(days=14))
    session_cookie_same_site: Literal["lax", "strict", "none"] = Field(default="lax")
    session_cookie_secure: bool = Field(default=False)
    session_serializer: str = Field(
        default="fastlife.session.serializer:SignedSessionSerializer"
    )
