import abc
from typing import Any, Mapping, Type

from fastapi import Request
from markupsafe import Markup
from pydantic.fields import FieldInfo


class AbstractTemplateRenderer(abc.ABC):
    route_prefix: str
    """Used to prefix url to fetch fast life widgets."""

    @abc.abstractmethod
    def render_page(self, request: Request, template: str, **params: Any) -> str:
        ...

    @abc.abstractmethod
    def render_template(self, template: str, **params: Any) -> str:
        ...

    @abc.abstractmethod
    def pydantic_form(
        self,
        model: Type[Any],
        form_data: Mapping[str, Any] | None = None,
        name: str | None = None,
        token: str | None = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        ...
