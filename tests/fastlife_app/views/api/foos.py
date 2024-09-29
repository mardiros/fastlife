from typing import Annotated

from fastapi import Body, Path, Response
from pydantic import BaseModel

from fastlife import resource, resource_view
from fastlife.config.configurator import ExternalDocs


class Ok(BaseModel):
    message: str = "Ok"


class Foo(BaseModel):
    name: str


instances: dict[str, Foo] = {}


@resource(
    "foos",
    collection_path="/foos",
    path="/foos/{name}",
    description="Manage foos, not bars.",
    external_docs=ExternalDocs(
        description="Discover what foos are at http://localhost/",
        url="http://localhost/",
    ),
)
class Foos:
    @resource_view(
        permission="foos:read",
        summary="API For foos",
        description="Fetch a list of foos.",
        response_description="foo collection",
    )
    async def collection_get(self, response: Response) -> list[Foo]:
        resp = list(instances.values())
        response.headers["Total-Count"] = "2"
        return resp

    @resource_view(
        permission="foos:write",
        summary="Register a foo.",
        description="The more the merrier.",
        response_description="ok",
    )
    async def collection_post(self, foo: Annotated[Foo, Body(...)]) -> Ok:
        instances[foo.name] = foo
        return Ok()

    @resource_view(
        permission="foos:read",
        summary="Get one foo by its name",
    )
    async def get(self, name: Annotated[str, Path(...)]) -> Foo:
        return instances[name]

    @resource_view(
        permission="foos:write",
        summary="Update a foo",
    )
    async def patch(
        self, name: Annotated[str, Path(...)], foo: Annotated[Foo, Body(...)]
    ) -> Ok:
        instance = instances.pop(name)
        instance.name = foo.name
        instances[instance.name] = instance
        return Ok()

    @resource_view(
        permission="foos:delete",
        summary="delete a foo",
    )
    async def delete(self, name: Annotated[str, Path(...)]) -> Ok:
        del instances[name]
        return Ok()

    @resource_view(
        summary="CORS preflight request",
        include_in_schema=False,
    )
    async def options(self, name: Annotated[str, Path(...)]) -> Ok:
        return Ok()
