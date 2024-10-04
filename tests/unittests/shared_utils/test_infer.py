from collections.abc import Mapping
from typing import Any, Union

import pytest

from fastlife.shared_utils.infer import is_union


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"type": int, "expected": False}, id="int"),
        pytest.param({"type": str, "expected": False}, id="str"),
        pytest.param({"type": int | str, "expected": True}, id="int | str"),
        pytest.param(
            {
                "type": Union[int, str],  # noqa: UP007
                "expected": True,
            },
            id="Union[int, str]",
        ),
    ],
)
def test_is_union(params: Mapping[str, Any]):
    assert is_union(params["type"]) is params["expected"]
