import abc

from starlette.types import Receive, Scope, Send


class AbstractMiddleware(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...
