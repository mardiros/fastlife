from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="fastlife_")

    template_search_path: str = Field(...)
    registry_class: str = Field(default="fastlife.configurator.registry:AppRegistry")
    template_renderer_class: str = Field(
        default="fastlife.templating.renderer.jinja2:Jinja2TemplateRenderer"
    )
