from datetime import timedelta
from typing import Literal, Type

from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from fastlife.configurator.base import AbstractMiddleware

from .serializer import AbsractSessionSerializer, SignedSessionSerializer


class SessionMiddleware(AbstractMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        cookie_name: str,
        secret_key: str,
        duration: timedelta,
        cookie_path: str = "/",
        cookie_same_site: Literal["lax", "strict", "none"] = "lax",
        cookie_secure: bool = False,
        cookie_domain: str = "",
        serializer: Type[AbsractSessionSerializer] = SignedSessionSerializer,
    ) -> None:
        self.app = app
        self.max_age = int(duration.total_seconds())
        self.serializer = serializer(secret_key, self.max_age)
        self.cookie_name = cookie_name
        self.security_flags = (
            f"Path={cookie_path}; HttpOnly; SameSite={cookie_same_site}"
        )
        if cookie_secure:
            self.security_flags += "; Secure"
        if cookie_domain:
            self.security_flags += f"; Domain={cookie_domain}"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return
        connection = HTTPConnection(scope)
        existing_session = self.cookie_name in connection.cookies
        if existing_session:
            data = connection.cookies[self.cookie_name].encode("utf-8")
            scope["session"], broken_session = self.serializer.deserialize(data)
            if broken_session:
                existing_session = False
        else:
            scope["session"] = {}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = None
                if scope["session"]:
                    # We have session data to persist.
                    data = self.serializer.serialize(scope["session"]).decode("utf-8")
                    headers = MutableHeaders(scope=message)
                    header_value = (
                        f"{self.cookie_name}={data}; "
                        f"Max-Age={self.max_age}; {self.security_flags}"
                    )
                    headers.append("set-cookie", header_value)
                elif existing_session:
                    # The session has been cleared.
                    headers = MutableHeaders(scope=message)
                    expires = "expires=Thu, 01 Jan 1970 00:00:00 GMT; "
                    header_value = (
                        f"{self.cookie_name}=; " f"{expires}{self.security_flags}"
                    )
                    headers.append("set-cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)
