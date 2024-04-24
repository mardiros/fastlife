from typing import Any, Optional, Type, Union
from pydantic import BaseModel
import pytest

from fastlife.shared_utils.infer import is_complex_type, is_union


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
def test_is_complex_type(typ: Type[Any], expected: bool):
    assert is_complex_type(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(bool, False, id="bool"),
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(str | int, True, id="str|int"),
        pytest.param(Union[str, int], True, id="Union[str, int]"),
        pytest.param(str | None, True, id="str|None"),
        pytest.param(Optional[str], True, id="Optional[str]"),
        pytest.param(DummyModel, False, id="DummyModel"),
        pytest.param(DummyModel | None, True, id="DummyModel|None"),
        pytest.param(DummyModel | str, True, id="DummyModel|str"),
    ],
)
def test_is_union(typ: Type[Any], expected: bool):
    assert is_union(typ) is expected
