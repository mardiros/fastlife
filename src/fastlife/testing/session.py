"""Session store for the webtest client."""

import time
from collections.abc import Mapping
from http.cookiejar import Cookie
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from .testclient import WebTestClient  # coverage: ignore


CookieTypes = httpx._types.CookieTypes  # type: ignore
Cookies = httpx._models.Cookies  # type: ignore


class Session(dict[str, Any]):
    """Manipulate the session of the WebTestClient browser."""

    def __init__(self, client: "WebTestClient"):
        self.client = client
        self.srlz = client.session_serializer
        self.settings = self.client.settings
        data: Mapping[str, Any]
        cookie_name = self.settings.session_cookie_name
        self.has_session = cookie_name in self.client.cookies
        if self.has_session:
            data, error = self.srlz.deserialize(
                self.client.cookies[cookie_name].encode("utf-8")
            )
            if error:
                self.has_session = False
        else:
            data = {}
        super().__init__(data)

    def __setitem__(self, __key: Any, __value: Any) -> None:
        """Initialize a value in the session of the client in order to test."""
        super().__setitem__(__key, __value)
        settings = self.settings
        data = self.serialize()
        self.client.cookies.jar.set_cookie(
            Cookie(
                version=0,
                name=settings.session_cookie_name,
                value=data,
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

    def serialize(self) -> str:
        """Serialize the session"""
        return self.srlz.serialize(self).decode("utf-8")
