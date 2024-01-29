from typing import Annotated

from fastapi import Depends, Response

from fastlife import Configurator, Template, configure, template
from tests.fastlife_app.security import AuthenticatedUser, authenticated_user


async def secured(
    template: Annotated[Template, template("secured.jinja2")],
    user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
) -> Response:
    return await template(user=user)


@configure
def includeme(config: Configurator):
    config.add_route(
        "secured_page", "/secured", secured, permission="admin", methods=["GET"]
    )
