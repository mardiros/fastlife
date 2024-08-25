import logging
from typing import Optional, Sequence, Tuple

from starlette.types import ASGIApp, Receive, Scope, Send

from fastlife.middlewares.base import AbstractMiddleware

log = logging.getLogger(__name__)


def get_header(headers: Sequence[Tuple[bytes, bytes]], key: bytes) -> Optional[str]:
    for hdr in headers:
        if hdr[0].lower() == key:
            return hdr[1].decode("latin1")
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
            new_vals = {
                "client": get_header(headers, b"x-real-ip"),
                "host": get_header(headers, b"x-forwarded-host"),
                "scheme": get_header(headers, b"x-forwarded-proto"),
            }
            scope.update({key: val for key, val in new_vals.items() if val is not None})

        await self.app(scope, receive, send)
