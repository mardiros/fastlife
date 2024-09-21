import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from fastlife import Configurator
from fastlife.config.configurator import Settings


def build_app():
    conf = Configurator(
        Settings(
            template_search_path="fastlife:templates,tests.fastlife_app:templates",
            session_secret_key="supasickret",
            check_permission="tests.fastlife_app.security:check_permission",
            jinjax_auto_reload=True,
            api_swagger_ui_url="/api/doc",
            api_redocs_url="/api/redoc",
        )
    )
    conf.include("tests.fastlife_app.views")
    conf.include("tests.fastlife_app.static")
    return conf.build_asgi_app()


app = build_app()


def main():
    config = Config()
    config.bind = ["0.0.0.0:8888", "[::1]:8888"]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve(app, config))  # type: ignore


if __name__ == "__main__":
    main()
