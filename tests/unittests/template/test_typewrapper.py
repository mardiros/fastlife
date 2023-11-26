from typing import Any, Mapping, Optional, Union

import pytest

from fastlife.templating.renderer.widgets.base import TypeWrapper
from tests.fastlife_app.models import Cat, Dog, Person


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
                "type": Person,
                "expected_fullname": "tests.fastlife_app.models:Person",
            },
            id="Person",
        ),
        pytest.param(
            {
                "type": Dog | Cat,
                "expected_fullname": "|".join(
                    ["tests.fastlife_app.models:Dog", "tests.fastlife_app.models:Cat"]
                ),
            },
            id="Dog | Cat",
        ),
        pytest.param(
            {
                "type": Union[Dog, Cat],
                "expected_fullname": "|".join(
                    ["tests.fastlife_app.models:Dog", "tests.fastlife_app.models:Cat"]
                ),
            },
            id="Union[Dog, Cat]",
        ),
        pytest.param(
            {
                "type": Optional[Dog],
                "expected_fullname": "|".join(
                    # Not sur that NoneType will be , id="Optional[Dog]"ok
                    ["tests.fastlife_app.models:Dog", "builtins:NoneType"]
                ),
            },
            id="Optional[Dog]",
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
            "expected_url": "/_/pydantic-form/widgets/builtins:str",
            "expected_params": {"name": "foo", "token": "xyz"},
        },
    ],
)
def test_typewrapper_url(params: Mapping[str, Any]):
    wrap = TypeWrapper(params["type"], route_prefix="/_", name="foo", token="xyz")
    assert wrap.url == params["expected_url"]
    assert wrap.params == params["expected_params"]
