import re
from typing import Any, Literal, Mapping
from urllib.parse import urlencode

import bs4
import httpx
from fastapi.testclient import TestClient
from starlette.types import ASGIApp


class WebForm:
    def __init__(self, client: "WebTestClient", origin: str, form: bs4.Tag):
        self._client = client
        self._form = form
        self._origin = origin
        self._formdata: dict[str, str] = {}
        inputs = self._form.find_all("input")
        for input in inputs:
            if input.attrs.get("type") == "checkbox" and "checked" not in input.attrs:
                continue
            self._formdata[input.attrs["name"]] = input.attrs.get("value", "")
        # field select, textearea...

    def set(self, fieldname: str, value: str) -> Any:
        if fieldname not in self._formdata:
            raise ValueError(f"{fieldname} does not exists")
        self._formdata[fieldname] = value

    def button(self, text: str) -> "WebForm":
        assert self._form.find("button", string=re.compile(f".*{text}.*")) is not None
        return self

    def submit(self, follow_redirects: bool = True) -> "WebResponse":
        target = (
            self._form.attrs.get("hx-post")
            or self._form.attrs.get("post")
            or self._origin
        )
        return self._client.post(
            target, data=self._formdata, follow_redirects=follow_redirects
        )


class WebResponse:
    def __init__(self, client: "WebTestClient", origin: str, response: httpx.Response):
        self._client = client
        self._response = response
        self._origin = origin
        self._html: bs4.BeautifulSoup | None = None
        self._form: WebForm | None = None

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def is_redirect(self) -> int:
        return 300 <= self._response.status_code < 400

    @property
    def content_type(self) -> str:
        return self._response.headers["content-type"]

    @property
    def headers(self) -> httpx.Headers:
        return self._response.headers

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def html(self) -> bs4.Tag:
        if self._html is None:
            self._html = bs4.BeautifulSoup(self._response.text, "html.parser")
        return self._html

    @property
    def html_body(self) -> bs4.Tag:
        body = self.html.find("body")
        assert body is not None
        assert isinstance(body, bs4.Tag)
        return body

    def by_text(self, text: str, *, node_name: str | None = None) -> bs4.Tag | None:
        nodes = self.html.find_all(string=re.compile(rf"\s*{text}\s*"))
        for node in nodes:
            if isinstance(node, bs4.NavigableString):
                node = node.parent

            if node_name:
                while node is not None:
                    if node.name == node_name:
                        return node
                    node = node.parent

        return None

    def by_label_text(self, text: str) -> bs4.Tag | None:
        label = self.by_text(text, node_name="label")
        assert label is not None
        assert label.attrs.get("for") is not None
        resp = self.html.find(id=label.attrs["for"])
        assert not isinstance(resp, bs4.NavigableString)
        return resp

    @property
    def form(self) -> WebForm:
        if self._form is None:
            form = self.html.form
            assert form is not None
            self._form = WebForm(self._client, self._origin, form)
        return self._form

    def by_node_name(
        self, node_name: str, *, attrs: dict[str, str] | None = None
    ) -> list[bs4.Tag]:
        return self.html.find_all(node_name, attrs or {})


CookieTypes = httpx._types.CookieTypes  # type: ignore
Cookies = httpx._models.Cookies  # type: ignore


class WebTestClient:
    def __init__(
        self,
        app: ASGIApp,
        cookies: CookieTypes | None = None,
    ) -> None:
        self.app = app
        self.testclient = TestClient(app, cookies=cookies or {})

    @property
    def cookies(self) -> Cookies:
        return self.testclient.cookies

    @cookies.setter
    def cookies(self, value: Cookies) -> None:
        self.testclient.cookies = value

    def request(
        self,
        method: Literal["GET", "POST"],  # I am a browser
        url: str,
        *,
        content: str | None = None,
        headers: Mapping[str, str] | None = None,
        max_redirects: int = 0,
    ) -> WebResponse:
        rawresp = self.testclient.request(
            method=method,
            url=url,
            headers=headers,
            content=content,
            follow_redirects=False,  # don't follow for cookie processing
        )
        # the wrapper client does not set cookies
        # and does not set cookie while redirecting,
        # so we reimplement it here
        if "set-cookie" in rawresp.headers:
            for name, cookie in rawresp.cookies.items():
                self.cookies.set(name, cookie)
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
        return resp

    def get(self, url: str, follow_redirects: bool = False) -> WebResponse:
        return self.request(
            "GET",
            url,
            max_redirects=int(follow_redirects) * 10,
        )

    def post(
        self, url: str, data: Mapping[str, Any], follow_redirects: bool = True
    ) -> WebResponse:
        return self.request(
            "POST",
            url,
            content=urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            max_redirects=int(follow_redirects) * 10,
        )
