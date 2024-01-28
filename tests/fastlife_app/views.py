from typing import Annotated, Optional

from fastapi import Depends, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from fastlife import Configurator, Template, configure, template
from fastlife.request.form_data import model
from tests.fastlife_app.models import Account
from tests.fastlife_app.security import (
    AuthenticatedUser,
    AuthenticationPolicy,
    authenticated_user,
)


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
    policy: Annotated[AuthenticationPolicy, Depends(AuthenticationPolicy)],
) -> Response:
    if loginform:
        if user := await policy.authenticate(
            loginform.username, loginform.password.get_secret_value()
        ):
            policy.remember(user)
        return RedirectResponse(request.url_for("secured_page"), status_code=303)
    return await template(model=LoginForm, form_data={})


async def secured(
    template: Annotated[Template, template("secured.jinja2")],
    user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
) -> Response:
    return await template(user=user)


async def logout(
    request: Request,
    policy: Annotated[AuthenticationPolicy, Depends(AuthenticationPolicy)],
) -> Response:
    policy.forget()
    return RedirectResponse(request.url_for("home"), status_code=302)


@configure
def includeme(config: Configurator):
    config.add_route("home", "/", hello_world, methods=["GET", "POST"])
    config.add_route("autoform", "/autoform", autoform, methods=["GET", "POST"])

    config.add_route("login", "/login", login, methods=["GET", "POST"])
    config.add_route(
        "secured_page", "/secured", secured, permission="admin", methods=["GET"]
    )
    config.add_route("logout", "/logout", logout, methods=["GET"])
