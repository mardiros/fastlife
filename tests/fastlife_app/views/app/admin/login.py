from typing import Annotated, Any, Mapping

from fastapi import Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from fastlife import Request, Response, view_config
from fastlife.request.form import FormModel, form_model
from tests.fastlife_app.services.uow import UnitOfWork, uow

UOW = Annotated[UnitOfWork, Depends(uow)]


class LoginForm(BaseModel):
    username: str
    password: SecretStr


@view_config("login", "/login", template="Login.jinja", methods=["GET", "POST"])
async def login(
    request: Request,
    loginform: Annotated[FormModel[LoginForm], form_model(LoginForm)],
    uow: UOW,
) -> Response | Mapping[str, Any]:
    assert request.security_policy
    if loginform.is_valid:
        if user := await uow.users.get_user_by_credencials(
            loginform.model.username, loginform.model.password.get_secret_value()
        ):
            await request.security_policy.remember(user)
        return RedirectResponse(request.url_for("secured_page"), status_code=303)
    return {"model": loginform}


@view_config("logout", "/logout", methods=["GET"])
async def logout(
    request: Request,
) -> Response:
    assert request.security_policy
    await request.security_policy.forget()
    return RedirectResponse(request.url_for("home"), status_code=302)