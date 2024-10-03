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


def view_config(
    name: str,
    path: str,
    *,
    permission: str | None = None,
    template: str | None = None,
    status_code: int | None = None,
    methods: list[str] | None = None,
) -> Callable[..., Any]:
    """
    A decorator function to add a view in the app.

    :param name: name of the route, used to build route from the helper
        {meth}`fastlife.request.request.Request.url_for` in order to create links.
    :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
        parameters.
    :param permission: a permission to validate by the
        {attr}`fastlife.config.settings.Settings.check_permission` function.
    :param methods: restrict route to a list of http methods.

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
            config.add_route(
                name=view_name,
                path=path,
                endpoint=ob,
                permission=permission,
                status_code=status_code,
                methods=methods,
                template=template,
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
