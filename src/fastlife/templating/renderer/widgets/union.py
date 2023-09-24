import secrets
from typing import Optional, Sequence, Type

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget, get_title


class TypeWrapper:
    def __init__(self, typ: Type[BaseModel]):
        self.typ = typ
        self.title = get_title(typ)
        self.id = f"{self.title.replace(' ', '-')}-{secrets.token_urlsafe(4)}".replace(
            "_", "-"
        )


class UnionWidget(Widget):
    def __init__(
        self,
        child: Optional[Sequence[Widget]],
        children_types: Sequence[Type[BaseModel]],
    ):
        self.child = child
        self.children_types = children_types

    @property
    def types(self) -> Sequence[TypeWrapper]:
        return [TypeWrapper(typ) for typ in self.children_types]

    def get_template(self) -> str:
        return "pydantic_form/union.jinja2"

    async def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version"""
        return Markup(
            await renderer.render_template(
                self.get_template(), widget=self, types=self.types, child=self.child
            )
        )
