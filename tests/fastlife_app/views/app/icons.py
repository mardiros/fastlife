from fastlife import JinjaXTemplate, Request, view_config


class IconsWall(JinjaXTemplate):
    template = "<IconsWall/>"


@view_config("icons", "/icons", methods=["GET"])
async def icons(request: Request) -> IconsWall:
    return IconsWall()
