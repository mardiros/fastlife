"""
Configure views using a decorator.

A simple usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import view_config


@view_config("hello_world", "/", methods=["GET"])
async def hello_world() -> Response:
    return Response("Hello World")
```
"""

from collections.abc import Callable
from typing import Any

import tamahagane as th

from fastlife.adapters.tamahagane.registry import TH_CATEGORY, THRegistry


def view_config(
    name: str,
    path: str,
    *,
    permission: str | None = None,
    status_code: int | None = None,
    methods: list[str] | None = None,
) -> Callable[..., Any]:
    """
    A decorator function to register a view in the
    {class}`Configurator <fastlife.config.configurator.GenericConfigurator>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

    :param name: name of the route, used to build route from the helper
        {meth}`fastlife.request.request.Request.url_for` in order to create links.
    :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
        parameters.
    :param permission: a permission to validate by the
        {class}`Security Policy <fastlife.service.security_policy.AbstractSecurityPolicy>`.
    :param status_code: customize response status code.
    :param methods: restrict route to a list of http methods.

    :return: the configuration callback.
    """
    view_name = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        def callback(registry: THRegistry) -> None:
            registry.fastlife.add_route(
                name=view_name,
                path=path,
                endpoint=wrapped,
                permission=permission,
                status_code=status_code,
                methods=methods,
            )

        th.attach(wrapped, callback, category=TH_CATEGORY)
        return wrapped

    return configure
