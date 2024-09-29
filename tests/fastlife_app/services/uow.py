from typing import Mapping

from pydantic import BaseModel


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


class UserRepository:
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> AuthenticatedUser | None:
        for user in USERS.values():
            if user.username == username and password == "secret":
                return user
        return None

    async def get_user_by_id(self, username: str) -> AuthenticatedUser | None:
        return USERS.get(username.lower())


class UnitOfWork:
    def __init__(self) -> None:
        self.users = UserRepository()


def uow() -> UnitOfWork:
    return UnitOfWork()
