# views.py
from pathlib import Path

from fastlife import Configurator, JinjaXTemplate, configure, view_config

templates_dir = Path(__file__).parent


class HelloWorld(JinjaXTemplate):
    template = "<Layout>Hello World</Layout>"


@view_config("hello_world", "/")
async def hello_world() -> HelloWorld:
    return HelloWorld()


@configure
def includeme(config: Configurator):
    config.add_template_search_path(templates_dir)
