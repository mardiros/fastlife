"""A dummy view to test the add_renderer"""

from collections.abc import Mapping
from typing import Any

from fastlife import view_config


@view_config("hello-f-string", "/f-string", template="hello.fstring", methods=["GET"])
async def hello_fstring() -> Mapping[str, Any]:
    return {"name": "world"}
