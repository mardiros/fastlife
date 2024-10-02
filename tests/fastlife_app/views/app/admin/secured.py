from typing import Annotated

from fastapi import Depends

from fastlife import Request
from fastlife.config.views import view_config
from fastlife.security.policy import Forbidden
from fastlife.services.templates import TemplateParams
from tests.fastlife_app.service.uow import AuthenticatedUser


async def authenticated_user(request: Request) -> AuthenticatedUser:
    assert request.security_policy
    ret = await request.security_policy.identity()
    if not ret:
        raise Forbidden()  # the route is protected by a permission, unreachable code
    return ret


User = Annotated[AuthenticatedUser, Depends(authenticated_user)]


@view_config(
    "secured_page",
    "/secured",
    permission="admin",
    template="Secured.jinja",
    methods=["GET"],
)
async def secured(
    user: User,
) -> TemplateParams:
    return {"user": user}
