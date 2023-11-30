import abc
from typing import Any, Mapping, Optional, Type

from fastapi import Request
from markupsafe import Markup


class AbstractTemplateRenderer(abc.ABC):
    route_prefix: str
    """Used to prefix url to fetch fast life widgets."""

    @abc.abstractmethod
    async def render_page(self, request: Request, template: str, **params: Any) -> str:
        ...

    @abc.abstractmethod
    async def render_template(self, template: str, **params: Any) -> str:
        ...

    @abc.abstractmethod
    async def pydantic_form(
        self,
        model: Type[Any],
        form_data: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
    ) -> Markup:
        ...
