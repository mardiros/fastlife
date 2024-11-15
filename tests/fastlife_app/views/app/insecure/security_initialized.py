from uuid import UUID

from pydantic import Field

from fastlife import Request, view_config
from fastlife.adapters.jinjax.inline import JinjaXTemplate
from tests.fastlife_app.models import BaseModel


class Person(BaseModel):
    id: UUID
    nick: str


class HelloWorld(JinjaXTemplate):
    template = "<HelloWorld :person='person'/>"
    person: Person | None = Field(default=None)


@view_config(
    "secured_pat_without_security_policy",
    "/permission-on-view",
    permission="admin",
    methods=["GET"],
)
async def permission_on_view_without_policy_installed() -> HelloWorld:
    return HelloWorld()


@view_config(
    "secured_pat_without_security_policy",
    "/request-has-permission",
    methods=["GET"],
)
async def request_has_permission_without_policy_installed(
    request: Request,
) -> HelloWorld:
    if await request.has_permission("yolo"):
        assert request.security_policy
        ident = await request.security_policy.identity()
        id = await request.security_policy.authenticated_userid()
        assert isinstance(id, UUID)
        return HelloWorld(person=Person(id=id, nick=str(ident)))
    return HelloWorld()
