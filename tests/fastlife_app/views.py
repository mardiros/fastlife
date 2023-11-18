from typing import Annotated, Optional

from fastapi import Response

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import FormModel, OptionalFormModel
from tests.fastlife_app.models import Person


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
) -> Response:
    return await template()


async def hello_name(
    template: Annotated[Template, template("hello_world.jinja2")],
    person: Annotated[Person, FormModel(Person)],
) -> Response:
    return await template(name=person.name)


async def autoform(
    template: Annotated[Template, template("autoform.jinja2")],
    person: Annotated[Optional[Person], OptionalFormModel(Person)],
):
    return await template(model=Person)


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET"])
    config.add_route("/", hello_name, methods=["POST"])

    config.add_route("/autoform", autoform, methods=["GET", "POST"])
