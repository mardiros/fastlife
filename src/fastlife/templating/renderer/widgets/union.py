import secrets
from typing import Optional, Sequence, Type

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget, get_title


class TypeWrapper:
    def __init__(self, typ: Type[BaseModel], route_prefix: str):
        self.typ = typ
        self.title = get_title(typ)
        self.id = f"{self.title.replace(' ', '-')}-{secrets.token_urlsafe(4)}".replace(
            "_", "-"
        )
        self.route_prefix = route_prefix

    @property
    def fullname(self) -> str:
        return f"{self.typ.__module__}:{self.typ.__name__}"

    def get_url(self, name: str) -> str:
        return f"{self.route_prefix}/pydantic-form/widgets/{self.fullname}?name={name}"


class UnionWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: str,
        child: Optional[Sequence[Widget]],
        children_types: Sequence[Type[BaseModel]],
    ):
        super().__init__(name, title=title)
        self.child = child
        self.children_types = children_types

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        return [TypeWrapper(typ, route_prefix) for typ in self.children_types]

    def get_template(self) -> str:
        return "pydantic_form/union.jinja2"

    async def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version"""
        return Markup(
            await renderer.render_template(
                self.get_template(),
                widget=self,
                types=self.build_types(renderer.route_prefix),
                child=self.child,
            )
        )
