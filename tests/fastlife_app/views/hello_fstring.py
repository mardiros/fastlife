"""A dummy view to test the add_renderer"""

from typing import Any, Mapping

from fastlife import view_config


@view_config("hello-f-string", "/f-string", template="hello.fstring", methods=["GET"])
async def hello_fstring() -> Mapping[str, Any]:
    return {"name": "world"}
