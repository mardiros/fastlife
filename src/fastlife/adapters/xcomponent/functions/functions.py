from typing import Any

from fastlife.adapters.xcomponent.registry import x_function


@x_function(name="len")
def length(sized: Any) -> int:
    return len(sized)


@x_function()
def is_bool(i: Any) -> bool:
    return isinstance(i, bool)


@x_function()
def is_str(value: Any) -> bool:
    return isinstance(value, str)
