from fastlife import Request, view_config
from fastlife.domain.model.template import JinjaXTemplate


class IconsWall(JinjaXTemplate):
    template = "<IconsWall/>"


@view_config("icons", "/icons", methods=["GET"])
async def icons(request: Request) -> IconsWall:
    return IconsWall()
