from typing import Any, Literal

import pytest
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core import InitErrorDetails

from fastlife.shared_utils.form import flatten_error


class Foo(BaseModel):
    name: str


class Bar(BaseModel):
    foos: list[Foo]


class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: int


class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: float


class PetsInside(BaseModel):
    pet: Cat | Dog = Field(discriminator="pet_type")
    n: int


class Model(BaseModel):
    foo: Foo


class ZipModel(BaseModel):
    zip: str = Field(min_length=3, max_length=5, pattern=r"^[0-9]+$")

    @field_validator("zip")
    @classmethod
    def validate(cls, value: Any) -> Any:
        errors: Any = [
            InitErrorDetails(
                type="string_too_short",
                loc=("zip",),
                input=value,
                ctx={"min_length": 3},
            ),
            InitErrorDetails(
                type="string_pattern_mismatch",
                loc=("zip",),
                input=value,
                ctx={"pattern": "^[0-9]+$"},
            ),
        ]
        raise ValidationError.from_exception_data("ZipModel", errors)


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
            id="nested-model",
        ),
        pytest.param(
            PetsInside,
            {"pet": {"pet_type": "cat"}},
            {
                "payload.n": "Field required",
                "payload.pet.meows": "Field required",
            },
            id="union missing field",
        ),
        pytest.param(
            PetsInside,
            {"pet": {"pet_type": "rabbit"}},
            {
                "payload.n": "Field required",
                "payload.pet": "Input tag 'rabbit' found using 'pet_type' does not match any of the "
                "expected tags: 'cat', 'dog'",
            },
            id="unknown discriminator",
        ),
        pytest.param(
            PetsInside,
            {"pet": {"name": "roger rabbit"}},
            {
                "payload.n": "Field required",
                "payload.pet": "Unable to extract tag using discriminator 'pet_type'",
            },
            id="missing discriminator",
        ),
        pytest.param(
            Model,
            {
                "foo": {"name": False},
            },
            {
                "payload.foo.name": "Input should be a valid string",
            },
            id="nested",
        ),
        pytest.param(
            ZipModel,
            {"zip": "337"},
            {
                "payload.zip": "String should have at least 3 characters, "
                "String should match pattern '^[0-9]+$'",
            },
        ),
    ],
)
def test_flatten_error(
    pydantic_model: type[BaseModel], data: dict[str, Any], expected: dict[str, str]
):
    exc = wrapme(pydantic_model, data)

    flattened = flatten_error(exc, "payload", pydantic_model)
    assert flattened == expected
