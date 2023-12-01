import abc
import secrets
from typing import Any, Mapping, Optional, Type

from markupsafe import Markup

from fastlife.shared_utils.infer import is_union
from fastlife.templating.renderer.abstract import AbstractTemplateRenderer


def get_title(typ: Type[Any]) -> str:
    return getattr(
        getattr(typ, "__meta__", None),
        "title",
        getattr(typ, "__name__", ""),
    )


class Widget(abc.ABC):
    name: str
    "variable name, nested variables have dots"
    title: str
    "Human title for the widget"
    aria_label: str
    "Non visible text alternative"
    token: str
    "unique token to ensure id are unique in the DOM"
    removable: bool
    "Indicate that the widget is removable from the dom"

    def __init__(
        self,
        name: str,
        *,
        title: Optional[str] = None,
        token: Optional[str] = None,
        aria_label: Optional[str] = None,
        removable: bool = False,
    ):
        self.name = name
        self.title = title or name.split(".")[-1]
        self.aria_label = aria_label or ""
        self.token = token or secrets.token_urlsafe(4).replace("_", "-")
        self.removable = removable

    @property
    def id(self) -> str:
        return f"{self.name}-{self.token}".replace("_", "-").replace(".", "-")

    @abc.abstractmethod
    def get_template(self) -> str:
        ...

    async def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version"""
        return Markup(await renderer.render_template(self.get_template(), widget=self))


def _get_fullname(typ: Type[Any]) -> str:
    if is_union(typ):
        typs = [_get_fullname(t) for t in typ.__args__]  # type: ignore
        return "|".join(typs)  # type: ignore
    return f"{typ.__module__}:{typ.__name__}"


class TypeWrapper:
    def __init__(self, typ: Type[Any], route_prefix: str, name: str, token: str):
        self.typ = typ
        self.route_prefix = route_prefix
        self.name = name
        self.title = get_title(typ)
        self.token = token

    @property
    def fullname(self) -> str:
        return _get_fullname(self.typ)

    @property
    def params(self) -> Mapping[str, str]:
        return {"name": self.name, "token": self.token}

    @property
    def url(self) -> str:
        ret = (
            f"{self.route_prefix}/pydantic-form/widgets/{self.fullname}"
            # f"?name={self.name}&token={self.token}"
        )
        return ret
