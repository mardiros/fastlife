from typing import Annotated

from fastapi import Response
from pydantic import BaseModel

from fastlife import Configurator, Template, configure, template
from fastlife.request.model_result import ModelResult, model
from tests.fastlife_app.models import Account, Group


class Person(BaseModel):
    nick: str


async def hello_world(
    template: Annotated[Template, template("HelloWorld")],
    person: Annotated[ModelResult[Person], model(Person, "person")],
) -> Response:
    return template(person=person.model)


async def autoform(
    template: Annotated[Template, template("AutoForm")],
    account: Annotated[ModelResult[Account], model(Account)],
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
