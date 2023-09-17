from typing import Any, Mapping, MutableMapping, Sequence, Tuple, cast
from urllib.parse import urlencode

import pytest
from fastapi import Request, APIRouter


@pytest.fixture()
def dummy_request_param(params: Mapping[str, Any]) -> Request:
    scope = {
        "type": "http",
        "headers": [("User-Agent", "Mozilla/5.0"), ("Accept", "text/html")],
        "router": APIRouter(),
        "query_string": b"",
        "scheme": "http",
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
    scope.update(req_params)
    return Request(scope)
