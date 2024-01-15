from typing import Annotated, Optional

from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

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


class LoginForm(BaseModel):
    username: str
    password: SecretStr


async def login(
    request: Request,
    loginform: Annotated[Optional[LoginForm], model(LoginForm)],
    template: Annotated[Template, template("login.jinja2")],
) -> Response:
    if loginform and loginform.password.get_secret_value() == "secret":
        request.session["username"] = loginform.username
        return RedirectResponse(request.url_for("secured"), status_code=303)
    return await template(model=LoginForm, form_data={})


async def secured(
    template: Annotated[Template, template("secured.jinja2")]
) -> Response:
    return await template()


@configure
def includeme(config: Configurator):
    config.add_route("/", hello_world, methods=["GET", "POST"])
    config.add_route("/autoform", autoform, methods=["GET", "POST"])

    config.add_route("/login", login, methods=["GET", "POST"])
    config.add_route("/secured", secured, methods=["GET"])
