"""
The configurator is here to register routes in a fastapi app,
with dependency injection.
"""
import logging

from fastapi import FastAPI
from venusian import Scanner  # type: ignore

log = logging.getLogger(__name__)


class Configurator(Scanner):
    app: FastAPI

    def __init__(self) -> None:
        super().__init__(  # type: ignore
            app=FastAPI(docs_url=None, redoc_url=None),
        )

    def get_app(self):
        return self.app
