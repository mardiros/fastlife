# file hello_world_with_template.py

from pathlib import Path

from fastlife import Configurator, Settings, TemplateParams

templates_dir = Path(__file__).parent / "templates"


async def hello_world() -> TemplateParams:
    return {}


def build_app():
    config = Configurator(Settings())
    config.add_template_search_path(templates_dir)
    config.add_route(
        "hello", "/", hello_world, template="HelloWorld.jinja", methods=["GET"]
    )
    return config.build_asgi_app()


app = build_app()
