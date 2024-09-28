import json
import os
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence, Tuple, Type, cast
from urllib.parse import urlencode

import pytest
from fastapi.requests import Request as FastApiRequest

from fastlife.config.registry import AppRegistry
from fastlife.config.settings import Settings
from fastlife.middlewares.session.serializer import AbsractSessionSerializer
from fastlife.request import Request
from fastlife.routing.router import Router
from fastlife.shared_utils.resolver import resolve


@pytest.fixture()
def root_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def python_path(root_dir: Path) -> None:
    os.environ["PYTHONPATH"] = str(root_dir / "tests")


@pytest.fixture()
def dummy_request_param(
    dummy_registry: AppRegistry,
    params: Mapping[str, Any],
) -> Request:
    scope = {
        "type": "http",
        "headers": [("user-agent", "Mozilla/5.0"), ("accept", "text/html")],
        "router": Router(),
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
            (key.lower().encode("latin-1"), val.encode("latin-1"))
            for key, val in headers.items()
        )
    body = req_params.pop("body", None)
    scope.update(req_params)
    req = Request(dummy_registry, FastApiRequest(scope))
    if body:
        req._body = body.encode("utf-8")  # type: ignore
    return req


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        template_search_path="fastlife:components,tests.fastlife_app:templates",
        session_secret_key="labamba",
        domain_name="testserver.local",
        session_cookie_domain="testserver.local",
    )


@pytest.fixture()
def dummy_registry(settings: Settings) -> AppRegistry:
    ret = AppRegistry(settings)
    ret.renderers[f".{settings.jinjax_file_ext}"] = resolve(  # type: ignore
        "fastlife.adapters.jinjax.renderer:JinjaxTemplateRenderer"
    )(settings)
    return ret


class DummySessionSerializer(AbsractSessionSerializer):
    def __init__(self, secret_key: str, max_age: int) -> None:
        ...

    def serialize(self, data: Mapping[str, Any]) -> bytes:
        return json.dumps(data).encode("utf-8")

    def deserialize(self, data: bytes) -> Tuple[Mapping[str, Any], bool]:
        ret: Mapping[str, Any] = json.loads(data)
        broken = "broken" in ret
        if broken:
            ret = {}
        return ret, broken


@pytest.fixture()
def dummy_session_serializer() -> Type[AbsractSessionSerializer]:
    return DummySessionSerializer
