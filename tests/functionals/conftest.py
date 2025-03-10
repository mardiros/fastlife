import socket
import threading
import time
from collections.abc import Iterator
from typing import Any

import pytest
import uvicorn
from tursu import tursu_collect_file

tursu_collect_file()

from tests.fastlife_app.entrypoint import app


def wait_for_socket(host: str, port: int, timeout: int = 5):
    """Wait until the socket is open before proceeding."""
    for _ in range(timeout * 10):  # Check every 0.1s for `timeout` seconds
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return  # Socket is open
        time.sleep(0.1)
    raise RuntimeError(f"Server on {host}:{port} did not start in time.")


@pytest.fixture(autouse=True)
def fastlife_app() -> Iterator[str]:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8888,
        loop="asyncio",
        lifespan="off",
        log_level="info",
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    wait_for_socket("127.0.0.1", 8888)
    yield "http://127.0.0.1:8888"
    server.should_exit = True
    thread.join()


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
