from typing import Annotated

from fastapi import Response

from fastlife import Configurator, Template, configure, template


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
) -> Response:
    return await template()


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world)
