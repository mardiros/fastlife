import logging
from collections.abc import Sequence

from fastlife.domain.model.asgi import ASGIApp, Receive, Scope, Send
from fastlife.middlewares.base import AbstractMiddleware

log = logging.getLogger(__name__)


def get_header(headers: Sequence[tuple[bytes, bytes]], key: bytes) -> str | None:
    for hkey, val in headers:
        if hkey.lower() == key:
            return val.decode("latin1")
    return None


def get_header_int(headers: Sequence[tuple[bytes, bytes]], key: bytes) -> int | None:
    for hkey, val in headers:
        if hkey.lower() == key:
            try:
                return int(val.decode("latin1"))
            except ValueError:
                break
    return None


class XForwardedStar(AbstractMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            headers = scope["headers"]
            x_real_ip = get_header(headers, b"x-real-ip")
            client = (
                (
                    x_real_ip,
                    get_header_int(headers, b"x-real-port")
                    or get_header_int(headers, b"x-forwarded-port")
                    or 0,
                )
                if x_real_ip
                else None
            )
            new_vals = {
                "client": client,
                "host": get_header(headers, b"x-forwarded-host"),
                "scheme": get_header(headers, b"x-forwarded-proto"),
            }
            scope.update({key: val for key, val in new_vals.items() if val is not None})

        await self.app(scope, receive, send)
