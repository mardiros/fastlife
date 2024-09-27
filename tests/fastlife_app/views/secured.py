from typing import Annotated

from fastapi import Depends, Response

from fastlife.config.views import view_config
from fastlife.templates import Template, template
from tests.fastlife_app.security import AuthenticatedUser, authenticated_user


@view_config("secured_page", "/secured", permission="admin", methods=["GET"])
async def secured(
    template: Annotated[Template, template("Secured.jinja")],
    user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
) -> Response:
    return template(user=user)
