from fastlife import Request, view_config
from fastlife.adapters.jinjax.renderer import JinjaXTemplate


class IconsWall(JinjaXTemplate):
    template = "<IconsWall/>"


@view_config("icons", "/icons", template="IconsWall.jinja", methods=["GET"])
async def icons(request: Request) -> IconsWall:
    return IconsWall()
