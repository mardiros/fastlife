from fastlife import Configurator, configure


@configure
def includeme(config: Configurator) -> None:
    config.include("fastlife.views.pydantic_form")
