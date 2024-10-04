from collections.abc import Mapping
from typing import Any

import pytest

from fastlife.middlewares.reverse_proxy.x_forwarded import XForwardedStar, get_header


@pytest.mark.parametrize(
    "headers,key,expected",
    [
        pytest.param([(b"a", b"A"), (b"b", b"B")], b"a", "A", id="basic"),
        pytest.param([(b"A", b"A"), (b"b", b"B")], b"a", "A", id="ci"),
        pytest.param([(b"a", b"A"), (b"b", b"B")], b"c", None, id="not found"),
        pytest.param(
            [(b"a", b"A"), (b"b", b"B")], b"A", None, id="key is case sensitive"
        ),
    ],
)
def test_get_header(headers: list[tuple[bytes, bytes]], key: bytes, expected: str):
    assert get_header(headers, key) == expected


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
                    "client": (None, None),
                },
            },
            id="no proxy headers",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "client": "127.0.0.1",
                    "headers": [(b"x-real-ip", b"1.2.3.4")],
                },
                "expected": {
                    "type": "http",
                    "client": ("1.2.3.4", None),
                    "headers": [(b"x-real-ip", b"1.2.3.4")],
                },
            },
            id="x-real-ip",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "client": "127.0.0.1",
                    "headers": [
                        (b"x-real-ip", b"1.2.3.4"),
                        (b"x-forwarded-port", b"80"),
                    ],
                },
                "expected": {
                    "type": "http",
                    "client": ("1.2.3.4", 80),
                    "headers": [
                        (b"x-real-ip", b"1.2.3.4"),
                        (b"x-forwarded-port", b"80"),
                    ],
                },
            },
            id="x-real-ip and port",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "client": "127.0.0.1",
                    "headers": [
                        (b"x-real-ip", b"1.2.3.4"),
                        (b"x-forwarded-port", b"heighty"),
                    ],
                },
                "expected": {
                    "type": "http",
                    "client": ("1.2.3.4", None),
                    "headers": [
                        (b"x-real-ip", b"1.2.3.4"),
                        (b"x-forwarded-port", b"heighty"),
                    ],
                },
            },
            id="x-real-ip and invalid port",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "headers": [(b"x-forwarded-host", b"ararat")],
                },
                "expected": {
                    "type": "http",
                    "host": "ararat",
                    "client": (None, None),
                    "headers": [(b"x-forwarded-host", b"ararat")],
                },
            },
            id="x-forwarded-host",
        ),
        pytest.param(
            {
                "scope": {
                    "type": "http",
                    "scheme": "http",
                    "headers": [(b"x-forwarded-proto", b"https")],
                },
                "expected": {
                    "type": "http",
                    "scheme": "https",
                    "client": (None, None),
                    "headers": [(b"x-forwarded-proto", b"https")],
                },
            },
            id="x-forwarded-scheme",
        ),
    ],
)
async def test_middleware(params: Mapping[str, Any]):
    data = {}

    async def app(scope: Mapping[str, Any], receive: Any, send: Any):
        data["scope"] = scope

    mid = XForwardedStar(app)
    await mid(params["scope"], None, None)  # type: ignore
    assert data["scope"] == params["expected"]
