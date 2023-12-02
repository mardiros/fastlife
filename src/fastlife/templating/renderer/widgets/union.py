from typing import Optional, Sequence, Type, Union

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import TypeWrapper, Widget


class UnionWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        child: Optional[Widget],
        children_types: Sequence[Type[BaseModel]],
        token: str,
        removable: bool,
    ):
        super().__init__(name, title=title, token=token, removable=removable)
        self.child = child
        self.children_types = children_types
        self.parent_name = name

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        return [
            TypeWrapper(typ, route_prefix, self.name, self.token)
            for typ in self.children_types
        ]

    def get_template(self) -> str:
        return "pydantic_form/union.jinja2"

    async def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version"""
        child = Markup(await self.child.to_html(renderer)) if self.child else ""
        return Markup(
            await renderer.render_template(
                self.get_template(),
                widget=self,
                types=self.build_types(renderer.route_prefix),
                parent_type=TypeWrapper(
                    Union[tuple(self.children_types)],  # type: ignore
                    renderer.route_prefix,
                    self.parent_name,
                    self.token,
                ),
                child=child,
            )
        )
