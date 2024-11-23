from collections.abc import Mapping
from datetime import timedelta
from typing import Any

import pytest
from starlette.types import ASGIApp

from fastlife.adapters.itsdangerous.session import SignedSessionSerializer
from fastlife.middlewares.session.middleware import SessionMiddleware
from fastlife.middlewares.session.serializer import AbsractSessionSerializer


@pytest.fixture
def dummy_asgi() -> tuple[ASGIApp, dict[str, Any]]:
    data: dict[str, Any] = {}

    async def app(scope: Mapping[str, Any], receive: Any, send: Any):
        data["scope"] = scope

    return app, data


@pytest.fixture
def asgi(dummy_asgi: tuple[ASGIApp, dict[str, Any]]) -> ASGIApp:
    return dummy_asgi[0]


@pytest.fixture
def asgi_data(dummy_asgi: tuple[ASGIApp, dict[str, Any]]) -> dict[str, Any]:
    return dummy_asgi[1]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "middleware_params": {
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=lax",
            },
            id="default",
        ),
        pytest.param(
            {
                "middleware_params": {
                    "cookie_secure": True,
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=lax; Secure",
            },
            id="secure",
        ),
        pytest.param(
            {
                "middleware_params": {
                    "cookie_domain": "foo.bar",
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=lax; Domain=foo.bar",
            },
            id="domain",
        ),
        pytest.param(
            {
                "middleware_params": {
                    "cookie_same_site": "strict",
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=strict",
            },
            id="strict",
        ),
        pytest.param(
            {
                "middleware_params": {
                    "cookie_secure": True,
                    "cookie_domain": "foo.bar",
                    "cookie_same_site": "strict",
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=strict; Secure; Domain=foo.bar",
            },
            id="all",
        ),
    ],
)
def test_security_flags(params: Mapping[str, Any], asgi: ASGIApp):
    mid = SessionMiddleware(
        app=asgi,
        cookie_name="s",
        duration=timedelta(hours=1),
        serializer=SignedSessionSerializer,
        **params["middleware_params"],
    )
    assert mid.security_flags == params["expected"]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {"scope": {"type": "ftp"}, "expected": {"type": "ftp"}}, id="unknown scope"
        ),
        pytest.param(
            {
                "scope": {"type": "http", "headers": []},
                "expected": {
                    "type": "http",
                    "headers": [],
                    "session": {},
                },
            },
            id="new session",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "headers": {b"cookie": b'sess={"broken":1}'}.items(),
                },
                "expected": {
                    "type": "http",
                    "headers": [(b"cookie", b'sess={"broken":1}')],
                    "session": {},
                },
            },
            id="broken session",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "headers": {b"cookie": b'sess={"ok":1}'}.items(),
                },
                "expected": {
                    "type": "http",
                    "headers": [(b"cookie", b'sess={"ok":1}')],
                    "session": {"ok": 1},
                },
            },
            id="existing session",
        ),
    ],
)
async def test_middleware(
    params: Mapping[str, Any],
    dummy_session_serializer: type[AbsractSessionSerializer],
    asgi: ASGIApp,
    asgi_data: dict[str, Any],
):
    mid = SessionMiddleware(
        app=asgi,
        cookie_name="sess",
        secret_key="x" * 16,
        duration=timedelta(hours=1),
        serializer=dummy_session_serializer,
    )
    await mid(params["scope"], None, None)  # type: ignore
    assert asgi_data["scope"] == params["expected"]
