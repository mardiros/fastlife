import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from fastlife import Configurator
from fastlife.config.configurator import Settings


async def app():
    conf = Configurator(
        Settings(
            template_search_path="fastlife:templates,tests.fastlife_app:templates",
            session_secret_key="supasickret",
            check_permission="tests.fastlife_app.security:check_permission",
            jinjax_auto_reload=True,
        )
    )
    conf.include("tests.fastlife_app.views")
    conf.include("tests.fastlife_app.static")
    app = conf.get_app()
    config = Config()
    config.bind = ["0.0.0.0:8888", "[::1]:8888"]
    await serve(app, config)  # type: ignore


def serve_app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app())


if __name__ == "__main__":
    serve_app()
