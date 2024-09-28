from typing import Annotated

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from fastlife import Configurator, Request, configure
from fastlife.config.exceptions import exception_handler
from fastlife.security.policy import (
    AbstractSecurityPolicy,
    Allowed,
    Denied,
    Forbidden,
    HasPermission,
    Unauthenticated,
    Unauthorized,
)


@exception_handler(Unauthorized)
def unauthorized_view(request: Request, exc: Unauthorized):
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.detail,
        headers={"WWW-Authenticate": "Bearer"},
    ) from exc


@exception_handler(Forbidden)
def forbidden_view(request: Request, exc: Forbidden):
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.detail,
        headers=exc.headers,
    ) from exc


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://token", scopes={"foo": "Foos resources"}, auto_error=False
)


class TokenInfo(BaseModel):
    username: str
    token: str


user_db = {
    "abc": TokenInfo(username="alice", token="abc"),
    "foobar": TokenInfo(username="foobar", token="foobar"),
}


def load_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenInfo:
    return user_db[token]


class OAuth2SecurityPolicy(AbstractSecurityPolicy[TokenInfo]):
    def __init__(
        self, request: Request, token: Annotated[str | None, Depends(oauth2_scheme)]
    ):
        super().__init__(request)
        self.token = token

    async def identity(self) -> TokenInfo | None:
        """Return app-specific user object."""
        return load_user(self.token) if self.token else None

    async def authenticated_userid(self) -> str | None:
        """Return a user identifier."""
        ident = await self.identity()
        return ident.username if ident else None

    async def has_permission(self, permission: str) -> type[HasPermission]:
        """Allow access to everything if signed in."""
        if not self.token:
            return Unauthenticated
        if self.token == "foobar":
            return Denied
        return Allowed

    async def remember(self, user: TokenInfo) -> None:
        """Save the user identity in the request session."""

    async def forget(self) -> None:
        """Destroy the request session."""


@configure
def includeme(config: Configurator):
    config.set_security_policy(OAuth2SecurityPolicy)
