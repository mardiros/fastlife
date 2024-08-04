from typing import Any

from fastapi import APIRouter

from fastlife.configurator.route_handler import FastlifeRoute


class FastLifeRouter(APIRouter):
    """The router used split your app in many routes."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs["route_class"] = FastlifeRoute
        super().__init__(**kwargs)
