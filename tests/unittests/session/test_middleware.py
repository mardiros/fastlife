from datetime import timedelta
from typing import Any, Mapping, Type

import pytest

from fastlife.session.middleware import SessionMiddleware
from fastlife.session.serializer import AbsractSessionSerializer


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "middleware_params": {
                    "app": None,
                    "cookie_name": "sess",
                    "duration": timedelta(hours=1),
                    "secret_key": "x" * 16,
                },
                "expected": "Path=/; HttpOnly; SameSite=lax",
            },
            id="default",
        ),
        pytest.param(
            {
                "middleware_params": {
                    "app": None,
                    "cookie_name": "sess",
                    "duration": timedelta(hours=1),
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
                    "app": None,
                    "cookie_name": "sess",
                    "duration": timedelta(hours=1),
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
                    "app": None,
                    "cookie_name": "sess",
                    "duration": timedelta(hours=1),
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
                    "app": None,
                    "cookie_name": "sess",
                    "duration": timedelta(hours=1),
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
def test_security_flags(params: Mapping[str, Any]):
    mid = SessionMiddleware(**params["middleware_params"])
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
    params: Mapping[str, Any], dummy_session_serializer: Type[AbsractSessionSerializer]
):
    data = {}

    async def app(scope: Mapping[str, Any], receive: Any, send: Any):
        data["scope"] = scope

    mid = SessionMiddleware(
        app,
        cookie_name="sess",
        secret_key="x" * 16,
        duration=timedelta(hours=1),
        serializer=dummy_session_serializer,
    )
    await mid(params["scope"], None, None)  # type: ignore
    assert data["scope"] == params["expected"]
