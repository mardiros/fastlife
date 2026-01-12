from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from fastlife.shared_utils.form import flatten_error


class Foo(BaseModel):
    name: str


class Bar(BaseModel):
    foos: list[Foo]


def wrapme(typ: type[BaseModel], data: dict[str, Any]):
    with pytest.raises(ValidationError) as ctx:
        typ.model_validate(data)
    return ctx.value


@pytest.mark.parametrize(
    "pydantic_model,data,expected",
    [
        pytest.param(
            Foo,
            {},
            {
                "payload.name": "Field required",
            },
            id="simple",
        ),
        pytest.param(
            Bar,
            {"foos": [{"name": "bar"}, {}]},
            {
                "payload.foos.1.name": "Field required",
            },
            id="simple",
        ),
    ],
)
def test_flatten_error(
    pydantic_model: type[BaseModel], data: dict[str, Any], expected: dict[str, str]
):
    exc = wrapme(pydantic_model, data)

    flattened = flatten_error(exc, "payload", pydantic_model)
    assert flattened == expected
