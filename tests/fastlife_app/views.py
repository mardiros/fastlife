from typing import Annotated, Optional

from fastapi import Response

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import model
from tests.fastlife_app.models import Account


async def hello_world(
    template: Annotated[Template, template("hello_world.jinja2")],
    account: Annotated[Optional[Account], model(Account, "account")],
) -> Response:
    return await template(account=account)


async def autoform(
    template: Annotated[Template, template("autoform.jinja2")],
    account: Annotated[Optional[Account], model(Account)],
):
    account = account
    return await template(
        model=Account, form_data={"payload": account.model_dump()} if account else {}
    )


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET", "POST"])
    config.add_route("/autoform", autoform, methods=["GET", "POST"])
