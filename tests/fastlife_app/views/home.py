from typing import Annotated, Optional

from fastapi import Response

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import model
from tests.fastlife_app.models import Account, Group


async def hello_world(
    template: Annotated[Template, template("HelloWorld")],
    account: Annotated[Optional[Account], model(Account, "account")],
) -> Response:
    return template(account=account)


async def autoform(
    template: Annotated[Template, template("AutoForm")],
    account: Annotated[Optional[Account], model(Account)],
):
    account = account or Account(
        username="", groups=[Group(name="admin"), Group(name="editor")]
    )
    return template(
        model=Account, form_data={"payload": account.model_dump()} if account else {}
    )


@configure
def includeme(config: Configurator):
    config.add_route("home", "/", hello_world, methods=["GET", "POST"])
    config.add_route("autoform", "/autoform", autoform, methods=["GET", "POST"])
