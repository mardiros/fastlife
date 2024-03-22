from typing import Any

import pytest
from fastapi import Request

from fastlife.configurator.registry import AppRegistry
from fastlife.templating.binding import get_page_template


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "headers": [("cookie", "csrf_token=xxxCsrfTokenxxx")],
            }
        }
    ],
)
async def test_get_csrf_token_reuse_token(
    dummy_request_param: Request, default_registry: AppRegistry
):
    template = get_page_template("Layout")
    renderer = template(default_registry, dummy_request_param)
    response = renderer()
    assert "set-cookie" in response.headers
    assert (
        response.headers["set-cookie"]
        == "csrf_token=xxxCsrfTokenxxx; Max-Age=900; Path=/; SameSite=strict"
    )


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "headers": [("cookie", "csrf_token=xxxCsrfTokenxxx")],
            }
        }
    ],
)
async def test_create_csrf_token(
    dummy_request_param: Request, default_registry: AppRegistry
):
    def create_token():
        return "xxxCsrfTokenxxx"

    template = get_page_template("Layout")
    renderer: Any = template(
        default_registry,
        dummy_request_param,
        _create_csrf_token=create_token,  # type: ignore
    )
    response = renderer()
    assert "set-cookie" in response.headers
    assert (
        response.headers["set-cookie"]
        == "csrf_token=xxxCsrfTokenxxx; Max-Age=900; Path=/; SameSite=strict"
    )


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "scheme": "https",
                "headers": [("cookie", "csrf_token=xxxCsrfTokenxxx")],
            }
        }
    ],
)
async def test_get_csrf_token_https(
    dummy_request_param: Request, default_registry: AppRegistry
):
    template = get_page_template("Layout")
    renderer = template(default_registry, dummy_request_param)
    response = renderer()
    assert "set-cookie" in response.headers
    assert (
        response.headers["set-cookie"]
        == "csrf_token=xxxCsrfTokenxxx; Max-Age=900; Path=/; SameSite=strict; Secure"
    )
