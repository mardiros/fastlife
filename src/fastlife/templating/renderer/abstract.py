import abc
from typing import Any, Mapping, Optional, Type

from fastapi import Request
from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife.request.model_result import ModelResult


class AbstractTemplateRenderer(abc.ABC):
    route_prefix: str
    """Used to buid pydantic form"""

    @abc.abstractmethod
    def render_template(
        self,
        template: str,
        *,
        globals: Optional[Mapping[str, Any]] = None,
        **params: Any,
    ) -> str:
        """
        Render the given template with the given params.

        While rendering templates, the globals parameter is keps by the instantiated
        renderer and sent to every rendering made by the request.
        This is used by the pydantic form method that will render other templates
        for the request.
        """

    @abc.abstractmethod
    def pydantic_form(
        self,
        model: ModelResult[Any],
        *,
        name: str | None = None,
        token: str | None = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        ...

    @abc.abstractmethod
    def pydantic_form_field(
        self,
        model: Type[Any],
        *,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        ...


class AbstractTemplateRendererFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        ...
