from collections.abc import Mapping
from typing import Any

import pytest
from starlette.types import Message, Send

from fastlife.domain.model.asgi import ASGIApp
from fastlife.middlewares.backend_tag import XBackendTag


@pytest.fixture()
def dummy_send(asgi_data):
    async def send(message: Message):
        asgi_data["message"] = message
        return message

    return send


@pytest.fixture
def asgi() -> ASGIApp:
    async def app(scope: Mapping[str, Any], receive: Any, send: Any):
        await send(scope["message"])

    return app


@pytest.fixture
def asgi_data() -> dict[str, Any]:
    return {}


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "message": {"type": "ftp"},
                "expected": {"type": "ftp"},
                "kwargs": {"tag": "server-1"},
            },
            id="unknown scope",
        ),
        pytest.param(
            {
                "message": {"type": "http.response.start", "headers": []},
                "kwargs": {"tag": "server-1"},
                "expected": {
                    "headers": [
                        (
                            b"x-backend-tag",
                            b"server-1",
                        ),
                    ],
                    "type": "http.response.start",
                },
            },
            id="tag",
        ),
        pytest.param(
            {
                "message": {"type": "http.response.start", "headers": []},
                "kwargs": {"tag": "server-fr-1", "header_name": "x-server-tag"},
                "expected": {
                    "headers": [
                        (
                            b"x-server-tag",
                            b"server-fr-1",
                        ),
                    ],
                    "type": "http.response.start",
                },
            },
            id="tag with header name",
        ),
    ],
)
async def test_middleware(
    params: Mapping[str, Any],
    asgi: ASGIApp,
    dummy_send: Send,
    asgi_data: dict[str, Any],
):
    mid = XBackendTag(app=asgi, **params["kwargs"])
    await mid({"message": params["message"]}, None, dummy_send)  # type: ignore
    assert asgi_data["message"] == params["expected"]
