import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from fastlife import Configurator
from fastlife.config.configurator import Settings


async def build_app():
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
    return conf.get_asgi_app()


app = build_app()


def main():

    config = Config()
    config.bind = ["0.0.0.0:8888", "[::1]:8888"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve(app, config))


if __name__ == "__main__":
    main()
