from collections.abc import Mapping
from typing import Any, NewType, Union
from uuid import UUID

import pytest

from fastlife.shared_utils.infer import is_union

UserId = NewType("UserId", UUID)


@pytest.mark.parametrize(
    "type,expected",
    [
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(int | str, True, id="int | str"),
        pytest.param(
            Union[int, str],  # noqa: UP007
            True,
            id="Union[int, str]",
        ),
    ],
)
def test_is_union(type: type[Any], expected: bool):
    assert is_union(type) is expected
