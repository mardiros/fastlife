import re
from collections.abc import MutableMapping
from typing import Any, Literal, Mapping
from urllib.parse import urlencode

import bs4
import httpx
from fastapi.testclient import TestClient
from starlette.types import ASGIApp

from fastlife.configurator.settings import Settings
from fastlife.session.serializer import AbsractSessionSerializer
from fastlife.shared_utils.resolver import resolve


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


class Session(dict[str, Any]):
    def __init__(self, client: "WebTestClient"):
        self.client = client
        if client.session_serializer is None:
            raise RuntimeError(
                "WebTestClient has not been initialize with the app settings, "
                "can't decode session"
            )

        self.srlz = client.session_serializer
        settings = self.client.settings
        assert settings is not None
        self.settings = settings
        data: Mapping[str, Any]
        if settings.session_cookie_name in self.client.cookies:
            data, exists = self.srlz.deserialize(
                self.client.cookies[settings.session_cookie_name].encode("utf-8")
            )
        else:
            data, exists = {}, False
        self.new_session = not exists
        super().__init__(data)

    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, __value)
        settings = self.settings
        data = self.serialize()
        if self.new_session:
            self.client.cookies.set(
                settings.session_cookie_name,
                data,
                settings.domain_name,
                settings.session_cookie_path,
            )
        else:
            self.client.cookies[settings.session_cookie_name] = data

    def serialize(self) -> str:
        return self.srlz.serialize(self).decode("utf-8")


class WebTestClient:
    def __init__(
        self,
        app: ASGIApp,
        *,
        settings: Settings | None = None,
        cookies: CookieTypes | None = None,
    ) -> None:
        self.app = app
        self.testclient = TestClient(app, cookies=cookies or {})
        self.settings = settings
        self.session_serializer: AbsractSessionSerializer | None = None
        if settings:
            self.session_serializer = resolve(settings.session_serializer)(
                settings.session_secret_key,
                int(settings.session_duration.total_seconds()),
            )

    @property
    def cookies(self) -> Cookies:
        return self.testclient.cookies

    @cookies.setter
    def cookies(self, value: Cookies) -> None:
        self.testclient.cookies = value

    @property
    def session(self) -> MutableMapping[str, Any]:
        return Session(self)

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

    def get(self, url: str, follow_redirects: bool = True) -> WebResponse:
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
