"""
FastApi router for fastlife application.

The aim of this router is get {class}`fastlife.routing.route.Route`
available in the FastApi request depency injection.
"""

from typing import Any

from fastapi import APIRouter

from fastlife.adapters.fastapi.routing.route import Route


class Router(APIRouter):
    """
    The router used split your app in many routes.
    """

    def __init__(self, **kwargs: Any) -> None:
        self._renderer_globals: dict[str, tuple[Any, bool]] = {}
        kwargs["route_class"] = Route
        super().__init__(**kwargs)

    def add_renderer_global(
        self, name: str, value: Any, *, evaluate: bool = True
    ) -> None:
        self._renderer_globals[name] = value, evaluate

    def get_renderer_globals(self) -> dict[str, tuple[Any, bool]]:
        return self._renderer_globals
