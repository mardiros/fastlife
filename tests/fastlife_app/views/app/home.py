from typing import Annotated

from fastapi import Response
from pydantic import BaseModel

from fastlife import Configurator, configure
from fastlife.request.form import FormModel, form_model
from fastlife.templates import Template, template
from tests.fastlife_app.models import Account, Group


class Person(BaseModel):
    nick: str


async def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> Response:
    return template(person=person.model)


async def autoform(
    template: Annotated[Template, template("AutoForm.jinja")],
    account: Annotated[FormModel[Account], form_model(Account)],
) -> Response:
    return template(
        model=account,
        globals={
            "groups": [
                Group(name="admin"),
                Group(name="editor"),
                Group(name="moderator"),
            ]
        },
    )


@configure
def includeme(config: Configurator):
    config.add_route("home", "/", hello_world, methods=["GET", "POST"])
    config.add_route("autoform", "/autoform", autoform, methods=["GET", "POST"])
