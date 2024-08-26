from fastlife import Configurator, Settings


async def hello_world():
    return {"message": "Hello World"}


def build_app():
    config = Configurator(Settings())
    config.add_route("hello", "/", hello_world, methods=["GET"])
    return config.get_asgi_app()


app = build_app()


if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve(app, Config()))
