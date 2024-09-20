from typing import Annotated

from fastapi import Request, Response
from pydantic import BaseModel, SecretStr

from fastlife import Template, template, view_config
from fastlife.config.views import view_config


class LoginForm(BaseModel):
    username: str
    password: SecretStr


@view_config("login", "/icons", methods=["GET"])
async def icons(
    request: Request,
    template: Annotated[Template, template("IconsWall")],
) -> Response:
    return template()
