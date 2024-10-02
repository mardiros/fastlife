from typing import Annotated

from fastapi import Depends, Response
from starlette.status import HTTP_303_SEE_OTHER

from fastlife import Configurator, Request, configure
from fastlife.config.exceptions import exception_handler
from fastlife.security.policy import AbstractSecurityPolicy, Unauthorized
from tests.fastlife_app.config import MyRequest
from tests.fastlife_app.service.uow import AuthenticatedUser
from tests.fastlife_app.views.api.security import (
    Allowed,
    Denied,
    HasPermission,
    MyRegistry,
    Unauthenticated,
)


class RedirectLogin(Unauthorized):
    """Own exception to attach the proper exception handler."""


@exception_handler(RedirectLogin)
def redict_login(request: Request, exception: RedirectLogin):
    return Response(
        "See Other",
        status_code=HTTP_303_SEE_OTHER,
        headers={"Location": str(request.url_for("login"))},
    )


class SecurityPolicy(AbstractSecurityPolicy[AuthenticatedUser, MyRegistry]):
    Unauthorized = RedirectLogin

    def __init__(self, request: MyRequest):
        super().__init__(request)
        self.uow = request.registry.uow

    async def identity(self) -> AuthenticatedUser | None:
        if "user_id" not in self.request.session:
            return None
        user_id = self.request.session["user_id"]
        return await self.uow.users.get_user_by_id(user_id)

    async def authenticated_userid(self) -> str | None:
        """
        Return app-specific user object or raise an HTTPException.
        """
        ident = await self.identity()
        return ident.username if ident else None

    async def has_permission(
        self, permission: str
    ) -> type[HasPermission] | HasPermission:
        """Allow access to everything if signed in."""

        user = await self.identity()
        if not user:
            return Unauthenticated

        if user.has_permission(permission):
            return Allowed

        return Denied(f"User not granted to perform {permission}")

    async def remember(self, user: AuthenticatedUser) -> None:
        self.request.session["user_id"] = user.user_id

    async def forget(self) -> None:
        self.request.session.clear()


@configure
def includeme(config: Configurator):
    config.set_security_policy(SecurityPolicy)
