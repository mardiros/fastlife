from typing import Annotated

from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from fastlife import Request, view_config
from fastlife.domain.model.template import JinjaXTemplate
from fastlife.request.form import FormModel, form_model
from tests.fastlife_app.config import MyRequest


class LoginForm(BaseModel):
    username: str
    password: SecretStr


class LoginTemplate(JinjaXTemplate):
    template = """<Login :model="model" />"""
    model: FormModel[LoginForm]


@view_config("login", "/login", methods=["GET", "POST"])
async def login(
    request: MyRequest,
    loginform: Annotated[FormModel[LoginForm], form_model(LoginForm)],
) -> LoginTemplate | RedirectResponse:
    assert request.security_policy
    if loginform.is_valid:
        if user := await request.registry.uow.users.get_user_by_credencials(
            loginform.model.username, loginform.model.password.get_secret_value()
        ):
            await request.security_policy.remember(user)
            return RedirectResponse(request.url_for("secured_page"), status_code=303)
        else:
            loginform.add_error("username", "Bad username or password.")
    return LoginTemplate(model=loginform)


@view_config("logout", "/logout", methods=["GET"])
async def logout(
    request: Request,
) -> RedirectResponse:
    assert request.security_policy
    await request.security_policy.forget()
    return RedirectResponse(request.url_for("home"), status_code=302)
