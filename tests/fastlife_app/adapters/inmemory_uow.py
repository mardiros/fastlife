from typing import Mapping

from tests.fastlife_app.config import MySettings
from tests.fastlife_app.domain.model import AuthenticatedUser
from tests.fastlife_app.service.uow import AbstractUnitOfWork, AbstractUserRepository

USERS: Mapping[str, AuthenticatedUser] = {
    "1": AuthenticatedUser(username="Bob", user_id="1", permissions={"admin"}),
    "2": AuthenticatedUser(username="Alice", user_id="2", permissions={"admin"}),
    "3": AuthenticatedUser(username="Roger", user_id="3", permissions=set()),
}


class UserRepository(AbstractUserRepository):
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> AuthenticatedUser | None:
        for user in USERS.values():
            if user.username == username and password == "secret":
                return user
        return None

    async def get_user_by_id(self, username: str) -> AuthenticatedUser | None:
        return USERS.get(username.lower())


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, settings: MySettings) -> None:
        self.users = UserRepository()
