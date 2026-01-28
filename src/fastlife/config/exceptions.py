"""Customize error pages."""

from collections.abc import Callable
from typing import Any

from fastlife.adapters.tamahagane import RegistryHub, th_attach


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

    def configure(wrapped: Callable[..., Any]) -> Callable[..., Any]:
        def callback(registry: RegistryHub) -> None:
            registry.fastlife.add_exception_handler(
                exception,
                wrapped,
                **({} if status_code is None else {"status_code": status_code}),
            )

        th_attach(wrapped, callback)
        return wrapped

    return configure
