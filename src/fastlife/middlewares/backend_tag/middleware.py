import logging

from fastlife.domain.model.asgi import ASGIApp, Message, Receive, Scope, Send
from fastlife.middlewares.base import AbstractMiddleware

log = logging.getLogger(__name__)


class XBackendTag(AbstractMiddleware):
    def __init__(
        self, app: ASGIApp, *, tag: str, header_name: str = "x-backend-tag"
    ) -> None:
        self.app = app
        self.header_name = header_name.encode()
        self.tag = tag.encode()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((self.header_name, self.tag))
            await send(message)

        await self.app(scope, receive, send_wrapper)
