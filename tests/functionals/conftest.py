import asyncio
import socket
from collections.abc import AsyncIterator
from typing import Any

import pytest
import uvicorn
from tursu import tursu_collect_file

from tests.fastlife_app.entrypoint import app

tursu_collect_file()


async def wait_for_socket(host: str, port: int, timeout: int = 5) -> None:
    """Wait until the socket is open before proceeding."""
    for _ in range(timeout * 10):  # Check every 0.1s for `timeout` seconds
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return  # Socket is open
        await asyncio.sleep(0.1)
    raise RuntimeError(f"Server on {host}:{port} did not start in time.")


@pytest.fixture(autouse=True)
async def fastlife_app() -> AsyncIterator[str]:
    host, port = "127.0.0.1", 8888
    config = uvicorn.Config(
        app, host=host, port=port, log_level="error", loop="asyncio"
    )
    server = uvicorn.Server(config)

    task = asyncio.create_task(server.serve())
    await wait_for_socket(host, port)

    yield f"http://{host}:{port}"

    server.should_exit = True
    await task


@pytest.fixture()
def response() -> Any:
    class Response:
        def __init__(self):
            self.r = None

        def get_response(self) -> None:
            return self.r

        def set_response(self, val: Any) -> None:
            self.r = val

    return Response()
