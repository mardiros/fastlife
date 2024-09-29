from fastlife import Request, TemplateParams, view_config


@view_config("icons", "/icons", template="IconsWall.jinja", methods=["GET"])
async def icons(request: Request) -> TemplateParams:
    return {}
