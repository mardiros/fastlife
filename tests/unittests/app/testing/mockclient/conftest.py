from typing import Any, Literal, Mapping

import httpx
import pytest
from fastapi import FastAPI
from multidict import MultiDict
from starlette.types import ASGIApp

from fastlife.configurator.settings import Settings
from fastlife.testing.testclient import WebResponse, WebTestClient

CookieTypes = httpx._types.CookieTypes  # type: ignore
Cookies = httpx._models.Cookies  # type: ignore


@pytest.fixture()
def client(app: FastAPI, settings: Settings):
    class FakeClient(WebTestClient):
        url: str
        data: Mapping[str, Any]
        headers: Mapping[str, Any] | None
        follow_redirects: bool

        def __init__(
            self,
            app: ASGIApp,
            *,
            settings: Settings | None = None,
            cookies: CookieTypes | None = None,
        ) -> None:
            super().__init__(app, settings=settings, cookies=cookies)
            self.data = {}

        def request(
            self,
            method: Literal["GET", "POST"],
            url: str,
            *,
            content: str | None = None,
            headers: Mapping[str, str] | None = None,
            max_redirects: int = 0,
        ) -> WebResponse:
            fields = [
                f"""<input type="text" name="{key}" value="{val}">"""
                for key, val in self.data.items()
            ]
            fields.append(f"""<input type="text" name="origin" value="{url}">""")

            form = "\n".join(fields)
            return WebResponse(
                self,
                url,
                httpx.Response(
                    200,
                    html=f"""<html><form>{form}</form></html>""",
                ),
            )

        def post(
            self,
            url: str,
            data: MultiDict[str],
            *,
            headers: Mapping[str, Any] | None = None,
            follow_redirects: bool = True,
        ) -> WebResponse:
            self.data = data
            return super().post(
                url, data, headers=headers, follow_redirects=follow_redirects
            )

    return FakeClient(app, settings=settings)
