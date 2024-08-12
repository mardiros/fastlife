from typing import Annotated

from fastapi import Request, Response
from pydantic import BaseModel, SecretStr

from fastlife import Configurator, Template, configure, template


class LoginForm(BaseModel):
    username: str
    password: SecretStr


async def icons(
    request: Request,
    template: Annotated[Template, template("IconsWall")],
) -> Response:
    return template()


@configure
def includeme(config: Configurator):
    config.add_route("login", "/icons", icons, methods=["GET"])
