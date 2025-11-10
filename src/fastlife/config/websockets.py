"""
Configure views using a decorator.

A simple usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import Template, template, view_config


@view_config("hello_world", "/", methods=["GET"])
async def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
) -> Response:
    return template()
```
"""

from collections.abc import Callable
from typing import Any

import venusian

from .configurator import VENUSIAN_CATEGORY, Configurator


def websocket_view(
    name: str,
    path: str,
) -> Callable[..., Any]:
    """
    A decorator function to register a websocket view in the
    {class}`Configurator <fastlife.config.configurator.GenericConfigurator>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

    Note that the current implementation does not support permission check using
    the security policy.

    :param name: name of the route, used to build route from the helper
        {meth}`fastlife.request.request.Request.url_for` in order to create links.
    :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
        parameters.

    :return: the configuration callback.
    """
    view_name = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: Callable[..., Any]
        ) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            config.add_websocket_route(
                name=view_name,
                path=path,
                endpoint=ob,
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
