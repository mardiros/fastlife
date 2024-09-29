from fastlife import Request, view_config
from fastlife.services.templates import TemplateParams


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
        return {}
    return {}
