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
        kwargs["route_class"] = Route
        super().__init__(**kwargs)
