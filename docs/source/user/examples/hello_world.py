# file hello_world.py

from fastlife import Configurator, Response, Settings


async def hello_world() -> Response:
    return Response("Hello World")


def build_app():
    config = Configurator(Settings())
    config.add_route("hello", "/", hello_world, methods=["GET"])
    return config.build_asgi_app()


app = build_app()
