"""Customize error pages."""

from collections.abc import Callable
from typing import Any

import venusian

from .configurator import VENUSIAN_CATEGORY, Configurator


def exception_handler(
    exception: type[Exception],
    *,
    status_code: int | None = None,
) -> Callable[..., Any]:
    """
    A decorator function to add an exception handler in the app.

    :param methods: restrict route to a list of http methods.

    :return: the configuration callback.
    """

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        def callback(
            scanner: venusian.Scanner, name: str, ob: Callable[..., Any]
        ) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            config.add_exception_handler(
                exception,
                wrapped,
                **({} if status_code is None else {"status_code": status_code}),
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
