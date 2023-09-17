import os
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence, Tuple, cast
from urllib.parse import urlencode

import pytest
from fastapi import APIRouter, Request

from fastlife.configurator.registry import AppRegistry
from fastlife.configurator.settings import Settings


@pytest.fixture()
def root_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def python_path(root_dir: Path) -> None:
    os.environ["PYTHONPATH"] = str(root_dir / "tests")


@pytest.fixture()
def dummy_request_param(params: Mapping[str, Any]) -> Request:
    scope = {
        "type": "http",
        "headers": [("User-Agent", "Mozilla/5.0"), ("Accept", "text/html")],
        "router": APIRouter(),
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "path": "/",
    }
    req_params: MutableMapping[str, Any] = params.get("request", {}).copy()
    if "querystring" in req_params:
        req_params["query_string"] = urlencode(req_params.pop("querystring")).encode(
            "utf-8"
        )
    if "headers" in req_params:
        headers: Mapping[str, str] = dict(req_params["headers"])
        headers = {
            **dict(cast(Sequence[Tuple[str, str]], scope["headers"])),
            **headers,
        }
        req_params["headers"] = list(
            (key.encode("latin-1"), val.encode("latin-1"))
            for key, val in headers.items()
        )
    body = req_params.pop("body", None)
    scope.update(req_params)
    req = Request(scope)
    if body:
        req._body = body.encode("utf-8")  # type: ignore
    return req


@pytest.fixture()
def default_registry():
    return AppRegistry(Settings())
