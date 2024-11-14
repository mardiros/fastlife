from typing import Annotated

from fastapi import Depends, Query, Response

from fastlife import Request
from fastlife.adapters.jinjax.inline import JinjaXTemplate
from fastlife.config.views import view_config
from fastlife.request.form import FormModel
from fastlife.security.policy import Forbidden
from tests.fastlife_app.service.uow import AuthenticatedUser
from tests.fastlife_app.views.app.home import Person, form_model


async def authenticated_user(request: Request) -> AuthenticatedUser:
    assert request.security_policy
    ret = await request.security_policy.identity()
    if not ret:
        raise Forbidden()  # the route is protected by a permission, unreachable code
    return ret


User = Annotated[AuthenticatedUser, Depends(authenticated_user)]


class Secured(JinjaXTemplate):
    template = """<Secured :user="user" />"""
    user: User


class HelloWorld(JinjaXTemplate):
    template = """<HelloWorld :user="user" :person="person" />"""
    user: User
    person: Person


@view_config(
    "secured_page",
    "/secured",
    permission="admin",
    methods=["GET", "POST"],
)
async def secured(
    request: Request,
    user: User,
    person: Annotated[FormModel[Person], form_model(Person)],
) -> Secured | Response:
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
    return Secured(user=user)


@view_config(
    "secured_hello",
    "/secured-hello",
    permission="admin",
    methods=["GET"],
)
async def secured_hello(
    user: User,
    nick: Annotated[str, Query(...)],
) -> HelloWorld:
    person = Person(nick=nick)
    return HelloWorld(user=user, person=person)
