from typing import Annotated

from fastlife import Configurator, Response, TemplateParams, configure, view_config
from fastlife.request.form import FormModel, form_model
from fastlife.templates import Template, template
from tests.fastlife_app.models import Account, Group, Person


@view_config("home", "/", methods=["GET", "POST"], template="HelloWorld.jinja")
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> TemplateParams:
    return {"person": person.model}


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
    config.add_route("autoform", "/autoform", autoform, methods=["GET", "POST"])
