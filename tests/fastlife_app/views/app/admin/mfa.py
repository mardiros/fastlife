from typing import Annotated

from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_303_SEE_OTHER

from fastlife import (
    FormModel,
    XTemplate,
    exception_handler,
    form_model,
    view_config,
)
from fastlife.domain.model.security_policy import MFARequired
from tests.fastlife_app.config import MyRequest
from tests.fastlife_app.domain.model import AuthnToken


class MfaForm(BaseModel):
    code: str


class LoginTemplate(XTemplate):
    template = """
    <Layout>
      <H2>second factor</H2>
      <div class="max-w-(--breakpoint-lg) mx-auto px-5 bg-white min-h-sceen">
        <Form hx-post>
          {globals.pydantic_form(model=model)}
          <Button aria-label="login">Login</Button>
        </Form>
      </div>
    </Layout>
    """
    model: FormModel[MfaForm]


@view_config("mfa", "/mfa", methods=["GET", "POST"])
async def mfa(
    request: MyRequest,
    loginform: Annotated[FormModel[MfaForm], form_model(MfaForm)],
) -> LoginTemplate | RedirectResponse:
    assert request.security_policy
    if loginform.is_valid:
        uow = request.registry.uow
        if loginform.model.code == "1234":
            claimed = await request.security_policy.claimed_identity()
            if claimed is None:
                loginform.set_fatal_error("Something went wrong")
            else:
                user = await uow.users.get_user_by_id(claimed.user_id)
                assert user

                token = AuthnToken(
                    user_id=claimed.user_id,
                    username=claimed.username,
                    permissions=user.permissions,
                )
                await uow.tokens.add(token)
                await request.security_policy.remember(token)
                return RedirectResponse(
                    request.url_for("secured_page"), status_code=303
                )

        else:
            loginform.add_error("code", "Invalid code.")
    return LoginTemplate(model=loginform)


@exception_handler(MFARequired)
def on_mfa_error(request: MyRequest, exc: MFARequired):
    raise HTTPException(
        status_code=HTTP_303_SEE_OTHER,
        detail=exc.detail,
        headers={"Location": str(request.url_for("mfa"))},
    ) from exc
