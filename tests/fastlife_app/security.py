from typing import Annotated, Mapping, Optional

from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel

from fastlife.security.policy import CheckPermissionHook


class AuthenticatedUser(BaseModel):
    user_id: str
    username: str
    permissions: set[str]

    def has_permission(self, permission_name: str) -> bool:
        return permission_name in self.permissions


USERS: Mapping[str, AuthenticatedUser] = {
    "1": AuthenticatedUser(username="Bob", user_id="1", permissions={"admin"}),
    "2": AuthenticatedUser(username="Alice", user_id="2", permissions={"admin"}),
    "3": AuthenticatedUser(username="Roger", user_id="3", permissions=set()),
}


class UnitOfWork:
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> AuthenticatedUser | None:
        for user in USERS.values():
            if user.username == username and password == "secret":
                return user
        return None

    async def get_user_by_id(self, username: str) -> AuthenticatedUser | None:
        return USERS.get(username.lower())


def uow() -> UnitOfWork:
    return UnitOfWork()


class AuthenticationPolicy:
    def __init__(self, request: Request, uow: Annotated[UnitOfWork, Depends(uow)]):
        self.request = request
        self.uow = uow

    async def authenticate(
        self, username: str, password: str
    ) -> Optional[AuthenticatedUser]:
        return await self.uow.get_user_by_credencials(username, password)

    async def authenticated_user(self) -> Optional[AuthenticatedUser]:
        if "user_id" not in self.request.session:
            return None
        user_id = self.request.session["user_id"]
        return await self.uow.get_user_by_id(user_id)

    def remember(self, user: AuthenticatedUser) -> None:
        self.request.session["user_id"] = user.user_id

    def forget(self) -> None:
        self.request.session.clear()


async def authenticated_user(
    policy: Annotated[AuthenticationPolicy, Depends(AuthenticationPolicy)]
) -> Optional[AuthenticatedUser]:
    return await policy.authenticated_user()


def check_permission(permission_name: str) -> CheckPermissionHook:
    """Check if the user has the given permission."""

    async def check_perm(
        request: Request,
        user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
    ) -> None:
        if not user:
            raise HTTPException(
                303, "See Other", {"Location": str(request.url_for("login"))}
            )
        if not user.has_permission(permission_name):
            raise HTTPException(403, "Forbidden")

    return check_perm
