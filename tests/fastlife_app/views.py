from typing import Annotated, Optional

from fastapi import Response

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import model
from tests.fastlife_app.models import Person


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
    person: Annotated[Optional[Person], model(Person, "person")],
) -> Response:
    return await template(person=person)


async def autoform(
    template: Annotated[Template, template("autoform.jinja2")],
    person: Annotated[Optional[Person], model(Person)],
):
    return await template(
        model=Person, form_data={"payload": person.model_dump()} if person else {}
    )


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET", "POST"])
    config.add_route("/autoform", autoform, methods=["GET", "POST"])
