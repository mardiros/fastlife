from typing import Annotated

from fastapi import Depends, Query, Response

from fastlife import Request
from fastlife.config.views import view_config
from fastlife.request.form import FormModel
from fastlife.security.policy import Forbidden
from fastlife.services.templates import TemplateParams
from tests.fastlife_app.service.uow import AuthenticatedUser
from tests.fastlife_app.views.app.home import Person, form_model


async def authenticated_user(request: Request) -> AuthenticatedUser:
    assert request.security_policy
    ret = await request.security_policy.identity()
    if not ret:
        raise Forbidden()  # the route is protected by a permission, unreachable code
    return ret


User = Annotated[AuthenticatedUser, Depends(authenticated_user)]


@view_config(
    "secured_page",
    "/secured",
    permission="admin",
    template="Secured.jinja",
    methods=["GET", "POST"],
)
async def secured(
    request: Request,
    user: User,
    person: Annotated[FormModel[Person], form_model(Person)],
) -> TemplateParams | Response:
    if request.method == "POST":
        return Response(
            "...",
            status_code=200,
            headers={
                "HX-Redirect": (
                    f"{request.url_for('secured_hello')}?nick={person.model.nick}"
                )
            },
        )
    return {"user": user}


@view_config(
    "secured_hello",
    "/secured-hello",
    permission="admin",
    template="HelloWorld.jinja",
    methods=["GET"],
)
async def secured_hello(
    user: User,
    nick: Annotated[str, Query(...)],
) -> TemplateParams:
    person = Person(nick=nick)
    return {"user": user, "person": person}
