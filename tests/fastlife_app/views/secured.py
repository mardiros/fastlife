from typing import Annotated

from fastapi import Depends, Response

from fastlife import Template, template
from fastlife.config.views import view_config
from tests.fastlife_app.security import AuthenticatedUser, authenticated_user


@view_config("secured_page", "/secured", permission="admin", methods=["GET"])
async def secured(
    template: Annotated[Template, template("Secured")],
    user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
) -> Response:
    return template(user=user)
