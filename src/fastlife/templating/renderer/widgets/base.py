import abc
import secrets
from typing import Any, Optional, Type

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer


def get_title(typ: Type[Any]) -> str:
    return getattr(
        getattr(typ, "__meta__", None),
        "title",
        typ.__name__,
    )


class Widget(abc.ABC):
    name: str
    "variable name, nested variables have dots"
    title: str
    "Human title for the widget"
    id: str
    "Unique id for the widget"

    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        id: Optional[str] = None,
        required: bool = False,
    ):
        self.name = name
        self.title = title or name.split(".")[-1]
        self.id = id or f"{name}-{secrets.token_urlsafe(4)}".replace("_", "-")
        self.required = required

    @abc.abstractmethod
    def get_template(self) -> str:
        ...

    async def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version"""
        return Markup(await renderer.render_template(self.get_template(), widget=self))
