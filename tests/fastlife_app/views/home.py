from typing import Annotated

from fastapi import Response
from pydantic import BaseModel

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import MappingFormData, ModelResult, model
from tests.fastlife_app.models import Account


class Person(BaseModel):
    nick: str


async def hello_world(
    template: Annotated[Template, template("HelloWorld")],
    person: Annotated[ModelResult[Person], model(Person, "person")],
) -> Response:
    return template(person=person.unwrap_or(None) if person else None)


async def autoform(
    template: Annotated[Template, template("AutoForm")],
    data: MappingFormData,
    account_result: Annotated[ModelResult[Account], model(Account)],
):
    errors = None
    if account_result:
        if account_result.is_err():
            errors = account_result.unwrap_err()
        else:
            account = account_result.unwrap()
            data = {"payload": account.model_dump()}
    return template(model=Account, form_data=data, form_errors=errors)


@configure
def includeme(config: Configurator):
    config.add_route("home", "/", hello_world, methods=["GET", "POST"])
    config.add_route("autoform", "/autoform", autoform, methods=["GET", "POST"])
