"""Build you own middleware."""

import abc

from fastlife.domain.model.asgi import Receive, Scope, Send


class AbstractMiddleware(abc.ABC):
    """
    Abstract Base Class that represent a fastlife middleware.

    Starlette provide a middleware stack but does not have an abstract base class.
    This is the only reason this class exists.

    Fastlife middleware are starlette middlewares.
    """

    @abc.abstractmethod
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Called every time an http request is reveived.

        This method before the request object even exists.
        """
