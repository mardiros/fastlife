import abc
from typing import Any

from fastapi import Request


class AbstractTemplateRenderer(abc.ABC):
    @abc.abstractmethod
    async def render_page(self, request: Request, template: str, **params: Any) -> str:
        ...

    @abc.abstractmethod
    async def render_template(self, template: str, **params: Any) -> str:
        ...
