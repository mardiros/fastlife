# views.py
from pathlib import Path

from fastlife import Configurator, configure, view_config

templates_dir = Path(__file__).parent


@view_config("hello_world", "/", template="HelloWorld.jinja")
async def hello_world() -> dict[str, str]:
    return {}


@configure
def includeme(config: Configurator):
    config.add_template_search_path(templates_dir)
