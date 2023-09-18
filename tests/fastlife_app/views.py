from typing import Annotated

from pydantic import BaseModel, Field
from fastapi import Response

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import FormModel


class Person(BaseModel):
    name: str = Field(...)


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
) -> Response:
    return await template()


async def hello_name(
    template: Annotated[Template, template("hello_world.jinja2")],
    person: Annotated[Person, FormModel(Person)],
) -> Response:
    return await template(name=person.name)


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET"])
    config.add_route("/", hello_name, methods=["POST"])
