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
