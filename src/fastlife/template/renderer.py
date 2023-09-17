import abc
from typing import Any


class AbstractTemplateRenderer(abc.ABC):
    @abc.abstractmethod
    async def render_template(self, template: str, **params: Any) -> str:
        ...
