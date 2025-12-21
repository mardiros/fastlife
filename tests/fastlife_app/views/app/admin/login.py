from typing import Annotated

from pydantic import BaseModel, SecretStr

from fastlife import (
    FormModel,
    RedirectResponse,
    Request,
    form_model,
    view_config,
)
from tests.fastlife_app.config import MyRequest

from .xcomponents import XSigninTemplate


class LoginForm(BaseModel):
    username: str
    password: SecretStr


class LoginTemplate(XSigninTemplate):
    template = """
    <Layout>
      <H2>Let's authenticate</H2>
      <div class="max-w-(--breakpoint-lg) mx-auto px-5 bg-white min-h-sceen">
        <Form hx-post>
          {globals.pydantic_form(model=model)}
          <Button aria-label="login">Login</Button>
        </Form>
      </div>
    </Layout>
    """
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
            await request.security_policy.pre_remember(user)
            return RedirectResponse(request.url_for("secured_page"), hx_redirect=True)
        else:
            if loginform.model.username == "root":
                loginform.set_fatal_error("Something went wrong")
            else:
                loginform.add_error("username", "Bad username or password.")
    return LoginTemplate(model=loginform)


@view_config("logout", "/logout", methods=["GET"])
async def logout(
    request: Request,
) -> RedirectResponse:
    assert request.security_policy
    await request.security_policy.forget()
    return RedirectResponse(request.url_for("home"))
