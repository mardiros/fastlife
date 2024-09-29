from uuid import UUID

from fastlife import Request, view_config
from fastlife.services.templates import TemplateParams
from tests.fastlife_app.models import BaseModel


class Person(BaseModel):
    id: UUID
    nick: str


@view_config(
    "secured_pat_without_security_policy",
    "/permission-on-view",
    permission="admin",
    template="HelloWorld.jinja",
    methods=["GET"],
)
async def permission_on_view_without_policy_installed() -> TemplateParams:
    return {}


@view_config(
    "secured_pat_without_security_policy",
    "/request-has-permission",
    template="HelloWorld.jinja",
    methods=["GET"],
)
async def request_has_permission_without_policy_installed(
    request: Request,
) -> TemplateParams:
    if await request.has_permission("yolo"):
        assert request.security_policy
        ident = await request.security_policy.identity()
        id = await request.security_policy.authenticated_userid()
        return {"person": Person(id=id, nick=str(ident))}  # type: ignore
    return {}
