"""Testing your application."""

from collections.abc import Mapping, MutableMapping
from typing import Any, Literal, Self
from urllib.parse import urlencode

import bs4
import httpx
from fastapi.testclient import TestClient
from multidict import MultiDict

from fastlife.domain.model.asgi import ASGIApp
from fastlife.middlewares.session.serializer import AbsractSessionSerializer
from fastlife.settings import Settings
from fastlife.shared_utils.resolver import resolve
from fastlife.testing.dom import Element
from fastlife.testing.form import WebForm
from fastlife.testing.session import Session

CookieTypes = httpx._types.CookieTypes  # type: ignore
Cookies = httpx._models.Cookies  # type: ignore


class WebResponse:
    """Represent an http response made by the WebTestClient browser."""

    def __init__(self, client: "WebTestClient", origin: str, response: httpx.Response):
        self._client = client
        self._response = response
        self._origin = origin
        self._html: bs4.BeautifulSoup | None = None
        self._form: WebForm | None = None

    @property
    def status_code(self) -> int:
        """Http status code."""
        return self._response.status_code

    @property
    def is_redirect(self) -> bool:
        """True for any kind of http redirect status."""
        return 300 <= self._response.status_code < 400

    @property
    def content_type(self) -> str:
        """Get the content type of the response, from the header."""
        return self._response.headers.get("content-type", "").split(";").pop(0)

    @property
    def headers(self) -> httpx.Headers:
        """All http headers of the response."""
        return self._response.headers

    @property
    def text(self) -> str:
        """Http response body."""
        return self._response.text

    @property
    def html(self) -> Element:
        """Http response body as an Element."""
        if self._html is None:
            self._html = bs4.BeautifulSoup(self._response.text, "html.parser")
        return Element(self._client, self._html)

    @property
    def html_body(self) -> Element:
        """The body element of the html response."""
        body = self.html.by_node_name("body")
        assert len(body) == 1, "body element not found or multiple body found"
        return body[0]

    @property
    def form(self) -> WebForm:
        """The form element of the html response."""
        if self._form is None:
            form = self.html.form
            assert form is not None, "form element not found"
            self._form = WebForm(self._client, self._origin, form)
        return self._form

    def by_text(self, text: str, *, node_name: str | None = None) -> Element | None:
        """Search a dom element by its text."""
        return self.html.by_text(text, node_name=node_name)

    def by_label_text(self, text: str) -> Element | None:
        """Search a dom element by its associated label text."""
        return self.html.by_label_text(text)

    def by_node_name(
        self, node_name: str, *, attrs: dict[str, str] | None = None
    ) -> list[Element]:
        """List dom element having the given node name, and eventually attributes."""
        return self.html.by_node_name(node_name, attrs=attrs)


class WebTestClient:
    """The fake browser used for testing purpose."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        settings: Settings | None = None,
        cookies: CookieTypes | None = None,
    ) -> None:
        self.app = app
        if settings is None:
            settings = Settings()
            settings.domain_name = settings.domain_name or "testserver.local"
        self.testclient = TestClient(
            app, base_url=f"http://{settings.domain_name}", cookies=cookies or {}
        )
        self.settings = settings
        self.session_serializer: AbsractSessionSerializer = resolve(
            settings.session_serializer
        )(
            settings.session_secret_key,
            int(settings.session_duration.total_seconds()),
        )

    @property
    def cookies(self) -> Cookies:
        """HTTP Cookies."""
        return self.testclient.cookies

    @property
    def session(self) -> MutableMapping[str, Any]:
        """Server session stored in a cookies."""
        return Session(self)

    def request(
        self,
        method: Literal["GET", "POST", "DELETE"],
        url: str,
        *,
        content: str | None = None,
        headers: Mapping[str, str] | None = None,
        max_redirects: int = 0,
    ) -> WebResponse:
        """Perform http requests."""
        rawresp = self.testclient.request(
            method=method,
            url=url,
            headers=headers,
            content=content,
            follow_redirects=False,
        )
        resp = WebResponse(
            self,
            url,
            rawresp,
        )
        if resp.is_redirect and max_redirects > 0:
            if resp.status_code != 307:
                method = "GET"
                headers = None
                content = None
            return self.request(
                method=method,
                url=resp.headers["location"],
                content=content,
                headers=headers,
                max_redirects=max_redirects - 1,
            )
        if "HX-Redirect" in resp.headers and max_redirects > 0:
            return self.request(
                method="GET",
                url=resp.headers["HX-Redirect"],
                content=None,
                headers=headers,
                max_redirects=max_redirects - 1,
            )

        return resp

    def get(self, url: str, follow_redirects: bool = True) -> WebResponse:
        """Perform http GET request."""
        return self.request(
            "GET",
            url,
            max_redirects=int(follow_redirects) * 10,
        )

    def delete(self, url: str, follow_redirects: bool = True) -> WebResponse:
        """Perform http DELETE request."""
        return self.request(
            "DELETE",
            url,
            max_redirects=int(follow_redirects) * 10,
        )

    def post(
        self,
        url: str,
        data: MultiDict[str],
        *,
        headers: Mapping[str, Any] | None = None,
        follow_redirects: bool = True,
    ) -> WebResponse:
        """Perform http POST request in "application/x-www-form-urlencoded" format."""
        if headers is None:
            headers = {}
        return self.request(
            "POST",
            url,
            content=urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded", **headers},
            max_redirects=int(follow_redirects) * 10,
        )

    def __enter__(self) -> Self:
        self.testclient.__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.testclient.__exit__()
