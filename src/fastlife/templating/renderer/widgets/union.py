from typing import Any, Optional, Sequence, Type, Union

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import TypeWrapper, Widget


class UnionWidget(Widget[Widget[Any]]):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        value: Optional[Widget[Any]],
        error: str | None = None,
        children_types: Sequence[Type[BaseModel]],
        token: str,
        removable: bool,
    ):
        super().__init__(
            name,
            value=value,
            error=error,
            title=title,
            token=token,
            removable=removable,
        )
        self.children_types = children_types
        self.parent_name = name

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        return [
            TypeWrapper(typ, route_prefix, self.name, self.token)
            for typ in self.children_types
        ]

    def get_template(self) -> str:
        return "pydantic_form.Union"

    def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version"""
        child = Markup(self.value.to_html(renderer)) if self.value else ""
        return Markup(
            renderer.render_template(
                self.get_template(),
                widget=self,
                types=self.build_types(renderer.route_prefix),
                parent_type=TypeWrapper(
                    Union[tuple(self.children_types)],  # type: ignore
                    renderer.route_prefix,
                    self.parent_name,
                    self.token,
                    title=self.title,
                ),
                child=child,
            )
        )
