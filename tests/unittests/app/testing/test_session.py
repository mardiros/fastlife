import time
from http.cookiejar import Cookie
from typing import Type

import pytest

from fastlife.config.settings import Settings
from fastlife.middlewares.session.serializer import AbsractSessionSerializer
from fastlife.testing.testclient import Session, WebTestClient


@pytest.fixture()
def session(
    settings: Settings,
    client: WebTestClient,
    sessdata: str,
    dummy_session_serializer: Type[AbsractSessionSerializer],
):
    client.session_serializer = dummy_session_serializer("", 0)
    client.cookies.jar.set_cookie(
        Cookie(
            version=0,
            name=settings.session_cookie_name,
            value=sessdata,
            port=None,
            port_specified=False,
            domain=f".{settings.session_cookie_domain}",
            domain_specified=True,
            domain_initial_dot=True,
            path="/",
            path_specified=True,
            secure=False,
            expires=int(time.time() + settings.session_duration.total_seconds()),
            discard=False,
            comment=None,
            comment_url=None,
            rest={"HttpOnly": None, "SameSite": "lax"},  # type: ignore
            rfc2109=False,
        )
    )
    return Session(client=client)


@pytest.mark.parametrize(
    "sessdata,expected",
    [
        pytest.param("{}", {}, id="empty"),
        pytest.param('{"a": "A"}', {"a": "A"}, id="data"),
        pytest.param('{"broken": true}', {}, id="broken session"),
    ],
)
def test_init_session(session: Session, expected: str):
    assert dict(session) == expected


def test_set_session(client: WebTestClient):
    session = Session(client)
    session["a"] = "A"
    resp = client.get("/")
    assert client.session_serializer.deserialize(
        resp._response.cookies["flsess"]  # type: ignore
    ) == ({"a": "A"}, False)
