from typing import Annotated

from fastapi import Depends, Query, Response
from pydantic import Field

from fastlife import (
    Authenticated,
    FormModel,
    JinjaXTemplate,
    PendingMFA,
    Request,
    form_model,
    view_config,
)
from tests.fastlife_app.service.uow import UserAccount
from tests.fastlife_app.views.app.home import Person


async def authenticated_user(request: Request) -> UserAccount:
    assert request.security_policy
    state = await request.security_policy.get_authentication_state()
    match state:
        case Authenticated(identity):
            return identity
        case PendingMFA(_):
            raise request.security_policy.MFARequired()
        case _:
            raise request.security_policy.Forbidden()


User = Annotated[UserAccount, Depends(authenticated_user)]


class Secured(JinjaXTemplate):
    template = """
    <Layout>
      <H1>Welcome back {{ authenticated_user.username }}!</H1>
      <A href="/admin/logout">logout</A>

      <H2>Say Hello too ?</H2>
      <Form  method="post">
        <Input name="payload.nick" label="Name" />
        <Button aria-label="submit">Submit</Button>
      </Form>

    </Layout>
    """
    person: Person | None = Field(default=None)


class HelloWorld(JinjaXTemplate):
    template = """
    <Layout>

      <H1>Hello {{ person.nick }}!</H1>

      <H2>{{ authenticated_user.username }}, Say Hello too ?</H2>
      <Form  method="post">
        <Input name="payload.nick" label="Name" />
        <Button aria-label="submit">Submit</Button>
      </Form>

    </Layout>
    """
    person: Person


@view_config(
    "secured_page",
    "/secured",
    permission="admin",
    methods=["GET", "POST"],
)
async def secured(
    request: Request,
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
    return Secured()


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
