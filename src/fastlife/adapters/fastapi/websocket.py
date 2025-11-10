from collections.abc import AsyncIterator, Awaitable, Iterable
from typing import Annotated, Any, Generic

from fastapi import Depends
from fastapi.websockets import WebSocket as BaseWebSocket
from starlette.responses import Response

from fastlife.service.registry import DefaultRegistry, TRegistry


class MyWebSocket(Generic[TRegistry]):
    registry: TRegistry

    def __init__(self, socket: BaseWebSocket) -> None:
        self._sock = socket
        self.registry = socket.scope["fastlife.registry"]

    async def accept(
        self,
        subprotocol: str | None = None,
        headers: Iterable[tuple[bytes, bytes]] | None = None,
    ) -> None:
        return await self._sock.accept(subprotocol, headers)

    def receive_text(self) -> Awaitable[str]:
        return self._sock.receive_text()

    def receive_bytes(self) -> Awaitable[bytes]:
        return self._sock.receive_bytes()

    def receive_json(self, mode: str = "text") -> Awaitable[Any]:
        return self._sock.receive_json(mode)

    def iter_text(self) -> AsyncIterator[str]:
        return self._sock.iter_text()  # coverage: ignore

    def iter_bytes(self) -> AsyncIterator[bytes]:
        return self._sock.iter_bytes()  # coverage: ignore

    def iter_json(self) -> AsyncIterator[Any]:
        return self._sock.iter_json()  # coverage: ignore

    def send_text(self, data: str) -> Awaitable[None]:
        return self._sock.send_text(data)

    def send_bytes(self, data: bytes) -> Awaitable[None]:
        return self._sock.send_bytes(data)

    def send_json(self, data: Any, mode: str = "text") -> Awaitable[None]:
        return self._sock.send_json(data, mode)

    def close(self, code: int = 1000, reason: str | None = None) -> Awaitable[None]:
        return self._sock.close()

    def send_denial_response(self, response: Response) -> Awaitable[None]:
        return self._sock.send_denial_response(response)  # coverage: ignore


def get_websocket(socket: BaseWebSocket) -> MyWebSocket[Any]:
    return MyWebSocket(socket)


WebSocket = Annotated[MyWebSocket[TRegistry], Depends(get_websocket)]
GenericWebSocket = WebSocket[DefaultRegistry]

__all__ = ["WebSocket", "GenericWebSocket"]
