from typing import Annotated, Any, Literal, NewType, Optional, Union
from uuid import UUID

import pytest
from pydantic import BaseModel

from fastlife.shared_utils.infer import (
    get_runtime_type,
    get_type_by_discriminator,
    is_complex_type,
    is_newtype,
    is_union,
)
from tests.fastlife_app.views.app.i18n.dummy_messages import gettext

UserId = NewType("UserId", UUID)


class DummyModel(BaseModel):
    name: str


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(bool, False, id="bool"),
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(str | int, True, id="str|int"),
        pytest.param(str | None, True, id="str|None"),
        pytest.param(DummyModel, True, id="DummyModel"),
        pytest.param(DummyModel | None, True, id="DummyModel|None"),
        pytest.param(DummyModel | str, True, id="DummyModel|str"),
    ],
)
def test_is_complex_type(typ: type[Any], expected: bool):
    assert is_complex_type(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(bool, False, id="bool"),
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(str | int, True, id="str|int"),
        pytest.param(Union[str, int], True, id="Union[str, int]"),  # noqa: UP007
        pytest.param(str | None, True, id="str|None"),
        pytest.param(Optional[str], True, id="Optional[str]"),  # noqa: UP045
        pytest.param(Optional[UserId], True, id="Optional[UserId]"),  # noqa: UP045
        pytest.param(DummyModel, False, id="DummyModel"),
        pytest.param(DummyModel | None, True, id="DummyModel|None"),
        pytest.param(DummyModel | str, True, id="DummyModel|str"),
    ],
)
def test_is_union(typ: type[Any], expected: bool):
    assert is_union(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(UUID, False, id="false"),
        pytest.param(UserId, True, id="true"),
    ],
)
def test_is_newtype(typ: type[Any], expected: bool):
    assert is_newtype(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(UUID, UUID, id="unwrapped"),
        pytest.param(UserId, UUID, id="wrapped"),
    ],
)
def test_get_runtime_type(typ: type[Any], expected: type[Any]):
    assert get_runtime_type(typ) == expected


class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: int


class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: float


class Lizard(BaseModel):
    pet_type: Literal["reptile", "lizard"]
    scales: bool


@pytest.mark.parametrize(
    "discriminant,discriminator,typ,expected",
    [
        pytest.param("cat", "pet_type", Cat | Dog, Cat, id="one"),
        pytest.param("lizard", "pet_type", Cat | Dog | Lizard, Lizard, id="multi"),
        pytest.param("cow", "pet_type", Cat | Dog, None, id="not found"),
        pytest.param(
            "dog",
            "pet_type",
            Annotated[Cat, gettext("The Cat")] | Annotated[Dog, gettext("The Dog")],  # type: ignore
            Dog,
            id="not found",
        ),
    ],
)
def test_get_type_by_discriminator(
    discriminant: str | int, discriminator: str, typ: type[Any], expected: type[Any]
):
    assert get_type_by_discriminator(discriminant, discriminator, typ) is expected
