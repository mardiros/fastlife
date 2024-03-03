import re
import time
from collections.abc import MutableMapping
from typing import Any, Iterator, Literal, Mapping, Optional, Sequence
from urllib.parse import urlencode

import bs4
import httpx
from fastapi.testclient import TestClient
from starlette.types import ASGIApp

from fastlife.configurator.settings import Settings
from fastlife.session.serializer import AbsractSessionSerializer
from fastlife.shared_utils.resolver import resolve


class Element:
    def __init__(self, client: "WebTestClient", tag: bs4.Tag):
        self._client = client
        self._tag = tag

    def click(self) -> "WebResponse":
        return self._client.get(self._tag.attrs["href"])

    @property
    def node_name(self) -> str:
        return self._tag.name

    @property
    def attrs(self) -> dict[str, str]:
        return self._tag.attrs

    @property
    def text(self) -> str:
        return self._tag.text.strip()

    @property
    def form(self) -> "Element | None":
        return Element(self._client, self._tag.form) if self._tag.form else None

    @property
    def h1(self) -> "Element":
        nodes = self.by_node_name("h1")
        assert len(nodes) == 1, f"Should have 1 <h1>, got {len(nodes)} in {self}"
        return nodes[0]

    @property
    def h2(self) -> Sequence["Element"]:
        return self.by_node_name("h2")

    @property
    def hx_target(self) -> Optional[str]:
        el: bs4.Tag | None = self._tag
        while el:
            if "hx-target" in el.attrs:
                ret = el.attrs["hx-target"]
                if ret == "this":
                    ret = el.attrs["id"]
                return ret
            el = el.parent
        return None

    def by_text(self, text: str, *, node_name: str | None = None) -> "Element | None":
        nodes = self.iter_all_by_text(text, node_name=node_name)
        return next(nodes, None)

    def iter_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Iterator[Element]":
        nodes = self._tag.find_all(string=re.compile(rf"\s*{text}\s*"))
        for node in nodes:
            if isinstance(node, bs4.NavigableString):
                node = node.parent

            if node_name:
                while node is not None:
                    if node.name == node_name:
                        yield Element(self._client, node)
                    node = node.parent
            elif node:
                yield Element(self._client, node)
        return None

    def get_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Sequence[Element]":
        nodes = self.iter_all_by_text(text, node_name=node_name)
        return list(nodes)

    def by_label_text(self, text: str) -> "Element | None":
        label = self.by_text(text, node_name="label")
        assert label is not None
        assert label.attrs.get("for") is not None
        resp = self._tag.find(id=label.attrs["for"])
        assert not isinstance(resp, bs4.NavigableString)
        return Element(self._client, resp) if resp else None

    def by_node_name(
        self, node_name: str, *, attrs: dict[str, str] | None = None
    ) -> list["Element"]:
        return [
            Element(self._client, e) for e in self._tag.find_all(node_name, attrs or {})
        ]

    def __repr__(self) -> str:
        return f"<{self.node_name}>"

    def __str__(self) -> str:
        return str(self._tag)


class WebForm:
    def __init__(self, client: "WebTestClient", origin: str, form: Element):
        self._client = client
        self._form = form
        self._origin = origin
        self._formfields: dict[str, Element] = {}
        self._formdata: dict[str, str] = {}
        inputs = self._form.by_node_name("input")
        for input in inputs:
            self._formfields[input.attrs["name"]] = input
            if input.attrs.get("type") == "checkbox" and "checked" not in input.attrs:
                continue
            self._formdata[input.attrs["name"]] = input.attrs.get("value", "")

        inputs = self._form.by_node_name("select")
        for input in inputs:
            self._formfields[input.attrs["name"]] = input
            for option in input.by_node_name("options"):
                if "selected" in option.attrs:
                    self._formdata[input.attrs["name"]] = option.attrs.get(
                        "value", option.text
                    )
        # field textearea...

    def set(self, fieldname: str, value: str) -> Any:
        if fieldname not in self._formfields:
            raise ValueError(f"{fieldname} does not exists")
        if self._formfields[fieldname].node_name == "select":
            raise RuntimeError(f"{fieldname} is a <select>, use select() instead")
        self._formdata[fieldname] = value

    def select(self, fieldname: str, value: str) -> Any:
        if fieldname not in self._formfields:
            raise ValueError(f"{fieldname} does not exists")
        if self._formfields[fieldname].node_name != "select":
            raise RuntimeError(
                f"{fieldname} is a <{self._formfields[fieldname]}>, use set() instead"
            )
        if "multiple" in self._formfields[fieldname].attrs:
            raise NotImplementedError
        for option in self._formfields[fieldname].by_node_name("option"):
            if option.text == value.strip():
                self._formdata[fieldname] = option.attrs.get("value", option.text)
                break
        else:
            raise ValueError(f'No option {value} in <select name="{fieldname}">')

    def button(self, text: str, position: int = 0) -> "WebForm":
        buttons = self._form.get_all_by_text(text, node_name="button")
        assert len(buttons) > position, f'Button "{text}" not found'
        button = buttons[position]
        if "name" in button.attrs:
            self._formdata[button.attrs["name"]] = button.attrs.get("value", "")
        return self

    def submit(self, follow_redirects: bool = True) -> "WebResponse":
        headers = {}
        target = (
            self._form.attrs.get("hx-post")
            or self._form.attrs.get("post")
            or self._origin
        )
        if "hx-post" in self._form.attrs:
            if hx_target := self._form.hx_target:
                headers["HX-Target"] = hx_target

        return self._client.post(
            target,
            data=self._formdata,
            headers=headers,
            follow_redirects=follow_redirects,
        )

    def __contains__(self, key: str) -> bool:
        return key in self._formdata


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
    def html(self) -> Element:
        if self._html is None:
            self._html = bs4.BeautifulSoup(self._response.text, "html.parser")
        return Element(self._client, self._html)

    @property
    def html_body(self) -> Element:
        body = self.html.by_node_name("body")
        assert len(body) == 1
        return body[0]

    @property
    def form(self) -> WebForm:
        if self._form is None:
            form = self.html.form
            assert form is not None
            self._form = WebForm(self._client, self._origin, form)
        return self._form

    def by_text(self, text: str, *, node_name: str | None = None) -> Element | None:
        return self.html.by_text(text, node_name=node_name)

    def by_label_text(self, text: str) -> Element | None:
        return self.html.by_label_text(text)

    def by_node_name(
        self, node_name: str, *, attrs: dict[str, str] | None = None
    ) -> list[Element]:
        return self.html.by_node_name(node_name, attrs=attrs)


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
        self.has_session = settings.session_cookie_name in self.client.cookies
        if self.has_session:
            data, error = self.srlz.deserialize(
                self.client.cookies[settings.session_cookie_name].encode("utf-8")
            )
            if error:
                self.has_session = False
        else:
            data = {}
        super().__init__(data)

    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, __value)
        settings = self.settings
        data = self.serialize()
        from http.cookiejar import Cookie

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
        # this does not work
        # self.client.cookies.set(
        #     settings.session_cookie_name,
        #     data,
        #     settings.session_cookie_domain,
        #     settings.session_cookie_path,
        # )

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
        if settings is None:
            settings = Settings()
            settings.domain_name = settings.domain_name or "testserver.local"
        self.testclient = TestClient(
            app, base_url=f"http://{settings.domain_name}", cookies=cookies or {}
        )
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
        return self.request(
            "GET",
            url,
            max_redirects=int(follow_redirects) * 10,
        )

    def post(
        self,
        url: str,
        data: Mapping[str, Any],
        *,
        headers: Mapping[str, Any] | None = None,
        follow_redirects: bool = True,
    ) -> WebResponse:
        if headers is None:
            headers = {}
        return self.request(
            "POST",
            url,
            content=urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded", **headers},
            max_redirects=int(follow_redirects) * 10,
        )
