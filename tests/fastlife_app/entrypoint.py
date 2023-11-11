import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from fastlife import Configurator
from fastlife.configurator.configurator import Settings


async def app():
    conf = Configurator(
        Settings(template_search_path="fastlife:templates,tests.fastlife_app:templates")
    )
    conf.include("tests.fastlife_app.views")
    app = conf.get_app()
    config = Config()
    config.bind = ["0.0.0.0:8888"]
    await serve(app, config)  # type: ignore


def serve_app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app())


if __name__ == "__main__":
    serve_app()
