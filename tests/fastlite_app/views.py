from fastapi import Response

from fastlife import Configurator
from fastlife.configurator.configurator import configure


async def hello_world() -> Response:
    return Response("Hello World!")


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world)
