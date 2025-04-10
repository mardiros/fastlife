from collections.abc import Mapping, MutableMapping, MutableSequence
from typing import Any

import pytest

from fastlife import Request
from fastlife.adapters.fastapi.form_data import (
    unflatten_mapping_form_data,
    unflatten_sequence_form_data,
    unflatten_struct,
)


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "flatten": {"a": 1, "b": "B"},
                "expected": {"a": 1, "b": "B"},
            },
            id="unflatten values",
        ),
        pytest.param(
            {
                "flatten": {"a.a": 1, "a.b": "B"},
                "expected": {"a": {"a": 1, "b": "B"}},
            },
            id="nested dict",
        ),
        pytest.param(
            {
                "flatten": {"a.a.a": 1, "a.a.b": "B"},
                "expected": {"a": {"a": {"a": 1, "b": "B"}}},
            },
            id="recursive nested dict",
        ),
        pytest.param(
            {
                "flatten": {"a.a.a": 1, "a.a.b": "B", "a.c": "C", "d": "D"},
                "expected": {
                    "a": {
                        "a": {"a": 1, "b": "B"},
                        "c": "C",
                    },
                    "d": "D",
                },
            },
            id="recursive and multilevel nested dict",
        ),
        pytest.param(
            {
                "flatten": {"0": "A", "1": "B", "2": "C"},
                "expected": ["A", "B", "C"],
            },
            id="list",
        ),
        pytest.param(
            {
                "flatten": {"a.0": "A", "a.1": "B", "a.2": "C"},
                "expected": {"a": ["A", "B", "C"]},
            },
            id="list nested",
        ),
        pytest.param(
            {
                "flatten": {"a.0.a": "A", "a.0.b": "B", "a.1.c": "C"},
                "expected": {"a": [{"a": "A", "b": "B"}, {"c": "C"}]},
            },
            id="list containing struct",
        ),
        pytest.param(
            {
                "flatten": {"a.0.0": "A", "a.0.1": "B", "a.1.0": "C"},
                "expected": {"a": [["A", "B"], ["C"]]},
            },
            id="list containing list of list",
        ),
        pytest.param(
            {
                "flatten": {"a.1": "C"},
                "expected": {"a": [None, "C"]},
            },
            id="list containing missing piece of list",
        ),
        pytest.param(
            {
                "flatten": {
                    "payload.name": "x",
                    "payload.pets.1.nick": "a",
                    "payload.pets.1.breed": "Labrador",
                },
                "expected": {
                    "payload": {
                        "name": "x",
                        "pets": [
                            None,
                            {
                                "nick": "a",
                                "breed": "Labrador",
                            },
                        ],
                    },
                },
            },
            id="list containing missing piece of list nested dict",
        ),
    ],
)
def test_unflatten_struct(params: Mapping[str, Any]):
    input_: MutableMapping[str, Any] | MutableSequence[Any] = (
        [] if isinstance(params["expected"], list) else {}
    )
    assert unflatten_struct(params["flatten"], input_) == params["expected"]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "flatten": {"a": 1, "b": "B"},
                "unflattened_output": [],
                "type": ValueError,
                "error": "{'a': 1, 'b': 'B'}: Not a list",
            },
            id="not a list",
        ),
        pytest.param(
            {
                "flatten": {"0": "A"},
                "unflattened_output": 42,
                "type": TypeError,
                "error": "<class 'int'>",
            },
            id="unflattened_output type error",
        ),
        pytest.param(
            {
                "flatten": {"a.a": "A"},
                "unflattened_output": 42,
                "type": TypeError,
                "error": "<class 'int'>",
            },
            id="unflattened_output nexted type error",
        ),
    ],
)
def test_unflatten_struct_error(params: Mapping[str, Any]):
    with pytest.raises(params["type"]) as ctx:
        unflatten_struct(params["flatten"], params["unflattened_output"])
    assert str(ctx.value) == params["error"]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {"content-type": "application/x-www-form-urlencoded"},
                    "body": "a.b=C&csrf_token=xxx",
                },
                "expected": {"a": {"b": "C"}},
            },
            id="dict",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {"content-type": "application/x-www-form-urlencoded"},
                    "body": "a.b=C&a.b=D&csrf_token=xxx",
                },
                "expected": {"a": {"b": ["C", "D"]}},
            },
            id="multidict",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {"content-type": "application/x-www-form-urlencoded"},
                    "body": "a.b[]=C&csrf_token=xxx",
                },
                "expected": {"a": {"b": ["C"]}},
            },
            id="multidict",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {"content-type": "application/x-www-form-urlencoded"},
                    "body": "a.b[]=C&a.b[]=D&csrf_token=xxx",
                },
                "expected": {"a": {"b": ["C", "D"]}},
            },
            id="multidict",
        ),
    ],
)
async def test_unflatten_mapping_form_data(
    params: Mapping[str, Any], dummy_request_param: Request
):
    assert await unflatten_mapping_form_data(dummy_request_param) == params["expected"]


@pytest.mark.parametrize(
    "params",
    [
        {
            "request": {
                "method": "POST",
                "headers": {"content-type": "application/x-www-form-urlencoded"},
                "body": "0.a=b&csrf_token=xxx",
            },
            "expected": [{"a": "b"}],
        }
    ],
)
async def test_unflatten_sequence_form_data(
    params: Mapping[str, Any], dummy_request_param: Request
):
    assert await unflatten_sequence_form_data(dummy_request_param) == params["expected"]
