# file hello_world_with_template.py

from pathlib import Path

from fastlife import Configurator, Settings, JinjaXTemplate

templates_dir = Path(__file__).parent / "templates"


class HelloWorld(JinjaXTemplate):
    template = """
    <!DOCTYPE html>
    <html>
        <body>
            Hello World
        </body>
    </html>
    """


async def hello_world() -> HelloWorld:
    return HelloWorld()


def build_app():
    config = Configurator(Settings())
    config.add_route("hello", "/", hello_world, methods=["GET"])
    return config.build_asgi_app()


app = build_app()
