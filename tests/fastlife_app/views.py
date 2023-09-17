from typing import Annotated

from fastapi import Form, Response

from fastlife import Configurator, Template, configure, template


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
) -> Response:
    return await template()


async def hello_name(
    template: Annotated[Template, template("hello_world.jinja2")],
    name: Annotated[str, Form()],
) -> Response:
    return await template(name=name)


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET"])
    config.add_route("/", hello_name, methods=["POST"])
