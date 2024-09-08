from fastlife import Configurator, Settings


async def hello_world():
    return {"message": "Hello World"}


def build_app():
    config = Configurator(Settings())
    config.add_route("hello", "/", hello_world, methods=["GET"])
    return config.get_asgi_app()


app = build_app()