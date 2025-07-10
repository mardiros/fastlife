from collections.abc import Iterable

from fastapi import Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from fastlife import resource, resource_view


class Ok(BaseModel):
    message: str = "Ok"


class Dummy(BaseModel):
    name: str


instances: list[Dummy] = [
    Dummy(name="Peter"),
    Dummy(name="Bonnie"),
    Dummy(name="Bob"),
]


@resource(
    "streams",
    collection_path="/streams",
    description="Stream some data.",
)
class Streams:
    @resource_view(
        permission="streams:read",
        summary="API For streams",
        description="Stream dummies.",
        response_description="dummies collection",
        response_model=list[Dummy],
    )
    async def collection_get(self, response: Response) -> StreamingResponse:
        def gen_resp() -> Iterable[str]:
            yield "["
            first = True
            for instance in instances:
                if not first:
                    yield ","
                first = False
                yield instance.model_dump_json()
            yield "]"

        return StreamingResponse(
            gen_resp(), headers={"content-type": "application/json"}
        )
