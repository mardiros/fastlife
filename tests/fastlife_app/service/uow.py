import abc
from uuid import UUID

from tests.fastlife_app.domain.model import AuthnToken, TokenInfo, UserAccount


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> UserAccount | None: ...

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> UserAccount | None: ...

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserAccount | None: ...


class AbstractTokensRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, id: UUID) -> AuthnToken | None: ...

    @abc.abstractmethod
    async def add(self, token: AuthnToken) -> AuthnToken | None: ...


class AbstractApiTokensRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_token(self, token: str) -> TokenInfo | None: ...

    @abc.abstractmethod
    async def add(self, token: TokenInfo) -> None: ...


class AbstractUnitOfWork:
    users: AbstractUserRepository
    tokens: AbstractTokensRepository
    api_tokens: AbstractApiTokensRepository
