import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from fastlife import Configurator
from fastlife.config.configurator import Settings


def build_app():
    conf = Configurator(
        Settings(
            session_secret_key="supasickret",
            jinjax_auto_reload=True,
        )
    )
    conf.add_template_search_path("tests.fastlife_app:templates")
    conf.include("tests.fastlife_app.adapters")
    conf.include("tests.fastlife_app.views", ignore=[".api", ".app.admin"])
    conf.include("tests.fastlife_app.views.api", route_prefix="/api")
    conf.include("tests.fastlife_app.views.app.admin", route_prefix="/admin")
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
