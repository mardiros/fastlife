from typing import Any, Callable

import venusian

from .configurator import VENUSIAN_CATEGORY, Configurator


def view_config(
    name: str,
    path: str,
    *,
    permission: str | None = None,
    status_code: int | None = None,
    methods: list[str] | None = None,
) -> Callable[..., Any]:
    view_name = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: Callable[..., Any]
        ) -> None:
            if not hasattr(scanner, "fastlife"):
                return
            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            config.add_route(
                name=view_name,
                path=path,
                endpoint=ob,
                permission=permission,
                status_code=status_code,
                methods=methods,
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
