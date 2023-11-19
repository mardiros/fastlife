from typing import Optional, Sequence, Type

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget, get_title


class TypeWrapper:
    def __init__(self, typ: Type[BaseModel], route_prefix: str, name: str, token: str):
        self.typ = typ
        self.route_prefix = route_prefix
        self.name = name
        self.title = get_title(typ)
        self.token = token

    @property
    def fullname(self) -> str:
        return f"{self.typ.__module__}:{self.typ.__name__}"

    @property
    def url(self) -> str:
        return (
            f"{self.route_prefix}/pydantic-form/widgets/{self.fullname}"
            f"?name={self.name}&token={self.token}"
        )


class UnionWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: str,
        child: Optional[Widget],
        children_types: Sequence[Type[BaseModel]],
        parent_type: Type[BaseModel],
        token: str,
    ):
        super().__init__(name, title=title, token=token)
        self.child = child
        self.children_types = children_types
        self.parent_type = parent_type
        self.parent_name = "-".join("-".split(name)[:-1])

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
                    self.parent_type,
                    renderer.route_prefix,
                    self.parent_name,
                    self.token,
                ),
                child=child,
            )
        )
