from typing import Any, Mapping, Optional, Union

import pytest

from fastlife.templating.renderer.widgets.base import TypeWrapper
from tests.fastlife_app.models import Account, Email, PhoneNumber


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "type": str,
                "expected_fullname": "builtins:str",
            },
            id="str",
        ),
        pytest.param(
            {
                "type": int,
                "expected_fullname": "builtins:int",
            },
            id="int",
        ),
        pytest.param(
            {
                "type": bool,
                "expected_fullname": "builtins:bool",
            },
            id="bool",
        ),
        pytest.param(
            {
                "type": Account,
                "expected_fullname": "tests.fastlife_app.models:Account",
            },
            id="Account",
        ),
        pytest.param(
            {
                "type": PhoneNumber | Email,
                "expected_fullname": "|".join(
                    [
                        "tests.fastlife_app.models:PhoneNumber",
                        "tests.fastlife_app.models:Email",
                    ]
                ),
            },
            id="PhoneNumber | Email",
        ),
        pytest.param(
            {
                "type": Union[PhoneNumber, Email],
                "expected_fullname": "|".join(
                    [
                        "tests.fastlife_app.models:PhoneNumber",
                        "tests.fastlife_app.models:Email",
                    ]
                ),
            },
            id="Union[PhoneNumber, Email]",
        ),
        pytest.param(
            {
                "type": Optional[PhoneNumber],
                "expected_fullname": "|".join(
                    # Not sur that NoneType will be , id="Optional[Dog]"ok
                    ["tests.fastlife_app.models:PhoneNumber", "builtins:NoneType"]
                ),
            },
            id="Optional[PhoneNumber]",
        ),
    ],
)
def test_typewrapper(params: Mapping[str, Any]):
    wrap = TypeWrapper(params["type"], route_prefix="/_", name="foo", token="xyz")
    assert wrap.fullname == params["expected_fullname"]


@pytest.mark.parametrize(
    "params",
    [
        {
            "type": str,
            "params": {
                "name": "foo",
                "token": "xyz",
                "title": "Foo",
            },
            "expected_url": "/_/pydantic-form/widgets/builtins:str",
            "expected_params": {
                "name": "foo",
                "token": "xyz",
                "title": "Foo",
            },
        },
    ],
)
def test_typewrapper_url(params: Mapping[str, Any]):
    wrap = TypeWrapper(params["type"], route_prefix="/_", **params["params"])
    assert wrap.url == params["expected_url"]
    assert wrap.params == params["expected_params"]
