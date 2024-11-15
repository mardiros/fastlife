from fastlife import Request, view_config
from fastlife.domain.model.template import JinjaXTemplate


class HelloWorld(JinjaXTemplate):
    template = "<HelloWorld/>"


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
        return HelloWorld()
    return HelloWorld()
