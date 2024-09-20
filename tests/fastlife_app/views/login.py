from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from fastlife import Template, template, view_config
from fastlife.request.form import FormModel, form_model
from tests.fastlife_app.security import AuthenticationPolicy


class LoginForm(BaseModel):
    username: str
    password: SecretStr


@view_config("login", "/login", methods=["GET", "POST"])
async def login(
    request: Request,
    loginform: Annotated[FormModel[LoginForm], form_model(LoginForm)],
    template: Annotated[Template, template("Login")],
    policy: Annotated[AuthenticationPolicy, Depends(AuthenticationPolicy)],
) -> Response:
    if loginform.is_valid:
        if user := await policy.authenticate(
            loginform.model.username, loginform.model.password.get_secret_value()
        ):
            policy.remember(user)
        return RedirectResponse(request.url_for("secured_page"), status_code=303)
    return template(model=loginform)


@view_config("logout", "/logout", methods=["GET"])
async def logout(
    request: Request,
    policy: Annotated[AuthenticationPolicy, Depends(AuthenticationPolicy)],
) -> Response:
    policy.forget()
    return RedirectResponse(request.url_for("home"), status_code=302)
