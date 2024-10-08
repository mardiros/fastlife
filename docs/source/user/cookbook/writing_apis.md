# Writing APIs

Even if its not its primary goal, fastlife includes helpers to expose
a rest API using the configurator and using a class based view.

## Setup api information

The configurator expose a
{meth}`Configurator.set_api_documentation_info
<fastlife.config.configurator.GenericConfigurator.set_api_documentation_info>`
method that serve to create the {term}`OpenAPI` informations and optionally
expose the documentation url using {term}`Swagger UI` or {term}`Redoc`.

```python
from fastlife import Configurator, configure

@configure
def includeme(config: Configurator):
    config.set_api_documentation_info(
        "Dummy API",
        "4.2",
        "Description of the API that support **markdown**.",
        summary="API for dummies",
        swagger_ui_url="/api/doc",
        redoc_url="/api/redoc",
    )
```

## Writing a single route

We can use the configurator method

{meth}`Configurator.add_api_route
<fastlife.config.configurator.GenericConfigurator.add_api_route>` to add routes.

:::{tip}
This method is compatible with the FastAPI router, there is only a `permission`
parameter added in order to be used with a {class}`SecurityPolicy
<fastlife.security.policy.AbtractSecurityPolicy>`.
:::

It differs from the {meth}`Configurator.add_route
<fastlife.config.configurator.GenericConfigurator.add_route>`, the method that register
classical views with templates.

Here is a simple example

```python
from pydantic import BaseModel

from fastlife import Configurator, configure


class Info(BaseModel):
    build: str


def info() -> Info:
    return Info(build="00d94f2")


@configure
def includeme(config: Configurator):
    config.add_api_route(
        "home",
        "/api",
        info,
        methods=["GET"],
        summary="Retrieve Build Information",
        description="Return application build information",
        response_description="Build Info",
        tags=["monitoring"],
    )
```

## Writing a resource

Fastlife expose a decorator to groups a set of method under a tag directly,
this is an opinionated way to write APIs in a rest resource style.

```python
from typing import Annotated

from fastapi import Body, Path, Response
from pydantic import BaseModel

from fastlife import resource, resource_view
from fastlife.config.openapiextra import ExternalDocs


class Ok(BaseModel):
    message: str = "Ok"


class Foo(BaseModel):
    name: str


@resource(
    "foos",
    collection_path="/foos",
    path="/foos/{name}",
    description="Manage foos, not bars.",
    external_docs=ExternalDocs(
        description="Discover what foos are at http://example.net/",
        url="http://example.net/",
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
        ...

    @resource_view(
        permission="foos:write",
        summary="Register a foo.",
        description="The more the merrier.",
        response_description="ok",
    )
    async def collection_post(self, foo: Annotated[Foo, Body(...)]) -> Ok:
        ...

    @resource_view(
        permission="foos:read",
        summary="Get one foo by its name",
    )
    async def get(self, name: Annotated[str, Path(...)]) -> Foo:
        ...

    @resource_view(
        summary="CORS preflight request",
        include_in_schema=False,
    )
    async def options(self, name: Annotated[str, Path(...)]) -> Ok:
        ...

```

The `@resource
<fastlife.config.resources.resource>` decorator is used to decorate a class that
have HTTP methods.

There is no base class here. To add a 'POST' method a `post` method has to be
added to the class. it is a class based view.

The `path` used is set on the `@resource
<fastlife.config.resources.resource>` decorator.

A resource also have a `collection_path` and have appropriate `collection_*`
methods too.

All the http verb are supported so `get`, `post`, `put`, `patch`, `delete`,
`head` and `options`, and has to be prefixed by collection for the
`collection_path` set on the `@resource
<fastlife.config.resources.resource>` decorator (
`collection_get`, `collection_post`, `collection_put`, `collection_patch`,
`collection_delete`, `collection_head` and `collection_options`).


Usually, the basic crud operation in a json/rest style api ares:

* a `collection_post` is implemented to add an object to the collection (store a new resource).
* a `collection_get` is implemented to retrieve a list partial objects, and have fields.
* a `get` is implemented to retrieve a single and full object.
* a `patch` or `put` is implemented to update a resource.
* a `delete` is implemented to remove a resource from the collection.

Other methods handle personal needs.

A basic crud example, included from the test suite is in the fastlife APIs
documentation as a reference: {mod}`fastlife.config.resources`.


## Security Policy

Usually, an API is private, it requires a secret to be consumed, it can be
an api key or an OAuth2. token, it usually requires an Authorization header.

To handle security, in fastlife, you have to register a Security Policy.
The security policy is per "route_prefix".

It means that the app can have many polices depending on tht included
path. It can have public pages without any policy, an admin part
with a specific policy and an api with another policy.

While including the pages with route_prefix

```python
from fastlife import Configurator, configure

@configure
def includeme(config: Configurator):
    config.include('.public_pages')
    config.include('.admin', route_prefix='/admin')
    config.include('.api', route_prefix='/api')
```


:::{caution}
Event if the `/api` route exists, and the swagger_ui_url point to "/api/doc",
it will always be in include withoute the route prefix.
:::


Now imagine that the api module contains a security policy, it will applied
only to the api routes.

For example:

```python
from pydantic import BaseModel

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from fastlife import Configurator, configure, DefaultRegistry, Request
from fastlife.security.policy import AbstractSecurityPolicy, Allowed, Unauthorized


class AuthenticatedUser(BaseModel):
    user_id: str


# the the auto_error to False to avoid the Depends raise a error it self,
# it is controlled by the `has_permission` alled made while checking the permission
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://token", scopes={"foo": "Foos resources"}, auto_error=False
)


class MySecurityPolicy(AbstractSecurityPolicy[AuthenticatedUser, DefaultRegistry]):

    def __init__(
        self,
        request: Request,
        token: Annotated[str | None, Depends(oauth2_scheme)]
    ):
        super().__init__(request)
        self.token = token

    async def identity(self) -> AuthenticatedUser | None:
        if token is None:
            return None
        return AuthenticatedUser(user_id=token)  # Don't do that in the real world

    @abc.abstractmethod
    async def authenticated_userid(self) -> str | None:
        return self.token  # Don't do that in the real world

    async def has_permission(
        self, permission: str
    ) -> type[HasPermission]:
        return Allowed if self.token else Unauthorized

    async def remember(self, user: TUser) -> None:
        return None

    async def forget(self) -> None:
        return None


@configure
def includeme(config: Configurator):
    config.set_security_policy(MySecurityPolicy)
```

The security policy constructor accept any FastAPI dependency and is
made to receive FastAPI security dependency to properly build the doc.
But for fine grained check, it is better to always set the auto_error
to `False` to give the maximum control of the security policy.


:::{hint}
In FastAPI, many things must be done in the proper order to work.

In fastlife it just doesn't matter, because fastlife will build the FastAPI
app in the proper order.
:::
