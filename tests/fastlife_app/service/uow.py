import abc

from tests.fastlife_app.domain.model import AuthenticatedUser, TokenInfo


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_user_by_credencials(
        self, username: str, password: str
    ) -> AuthenticatedUser | None:
        ...

    @abc.abstractmethod
    async def get_user_by_id(self, username: str) -> AuthenticatedUser | None:
        ...


class AbstractTokensRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_token(self, token: str) -> TokenInfo | None:
        ...


class AbstractUnitOfWork:
    users: AbstractUserRepository
    tokens: AbstractTokensRepository
