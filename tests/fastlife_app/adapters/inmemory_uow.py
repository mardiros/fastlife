from collections.abc import Mapping
from uuid import UUID

from tests.fastlife_app.config import MySettings
from tests.fastlife_app.domain.model import AuthnToken, TokenInfo, UserAccount
from tests.fastlife_app.service.uow import (
    AbstractApiTokensRepository,
    AbstractTokensRepository,
    AbstractUnitOfWork,
    AbstractUserRepository,
)

USERS: Mapping[UUID, UserAccount] = {
    UUID(int=1): UserAccount(
        username="Bob", user_id=UUID(int=1), permissions={"admin"}
    ),
    UUID(int=2): UserAccount(
        username="Alice", user_id=UUID(int=2), permissions={"admin"}
    ),
    UUID(int=3): UserAccount(username="Roger", user_id=UUID(int=3), permissions=set()),
}

TOKENS: dict[UUID, AuthnToken] = {}
API_TOKENS: dict[str, TokenInfo] = {}


class UserRepository(AbstractUserRepository):
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> UserAccount | None:
        for user in USERS.values():
            if user.username == username and password == "secret":
                return user
        return None

    async def get_user_by_username(self, username: str) -> UserAccount | None:
        for user in USERS.values():
            if user.username == username:
                return user
        return None

    async def get_user_by_id(self, user_id: UUID) -> UserAccount | None:
        return USERS.get(user_id)


class TokensRepository(AbstractTokensRepository):
    async def get_by_id(self, id: UUID) -> AuthnToken | None:
        return TOKENS.get(id)

    async def add(self, token: AuthnToken) -> None:
        TOKENS[token.authntoken_id] = token
        return None


class APITokensRepository(AbstractApiTokensRepository):
    async def get_by_token(self, token: str) -> TokenInfo | None:
        return API_TOKENS.get(token)

    async def add(self, token: TokenInfo) -> None:
        API_TOKENS[token.token] = token
        return None


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, settings: MySettings) -> None:
        self.users = UserRepository()
        self.tokens = TokensRepository()
        self.api_tokens = APITokensRepository()
