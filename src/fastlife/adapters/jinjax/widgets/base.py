"""Widget base class."""
import abc
import secrets
from typing import Any, Generic, Mapping, Type, TypeVar

from markupsafe import Markup

from fastlife.services.templates import AbstractTemplateRenderer
from fastlife.shared_utils.infer import is_union

T = TypeVar("T")


def get_title(typ: Type[Any]) -> str:
    return getattr(
        getattr(typ, "__meta__", None),
        "title",
        getattr(typ, "__name__", ""),
    )


class Widget(abc.ABC, Generic[T]):
    """
    Base class for widget of pydantic fields.

    :param name: field name.
    :param value: field value.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param value: current value.
    :param error: error of the value if any.
    :param children_types: childrens types list.
    :param removable: display a button to remove the widget for optional fields.
    :param token: token used to get unique id on the form.
    """

    name: str
    "variable name, nested variables have dots."
    value: T | None
    """Value of the field."""
    title: str
    "Human title for the widget."
    hint: str
    "A help message for the the widget."
    aria_label: str
    "Non visible text alternative."
    token: str
    "unique token to ensure id are unique in the DOM."
    removable: bool
    "Indicate that the widget is removable from the dom."

    def __init__(
        self,
        name: str,
        *,
        value: T | None = None,
        error: str | None = None,
        title: str | None = None,
        hint: str | None = None,
        token: str | None = None,
        aria_label: str | None = None,
        removable: bool = False,
    ):
        self.name = name
        self.value = value
        self.error = error
        self.title = title or name.split(".")[-1]
        self.hint = hint or ""
        self.aria_label = aria_label or ""
        self.token = token or secrets.token_urlsafe(4).replace("_", "-")
        self.removable = removable
        self.id = f"{self.name}-{self.token}".replace("_", "-").replace(".", "-")

    @abc.abstractmethod
    def get_template(self) -> str:
        """Get the widget component template."""

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version."""
        return Markup(renderer.render_template(self.get_template(), widget=self))


def _get_fullname(typ: Type[Any]) -> str:
    if is_union(typ):
        typs = [_get_fullname(t) for t in typ.__args__]  # type: ignore
        return "|".join(typs)  # type: ignore
    return f"{typ.__module__}:{typ.__name__}"


class TypeWrapper:
    """
    Wrap children types for union type.

    :param typ: Wrapped type.
    :param route_prefix: route prefix used for ajax query to build type.
    :param name: name of the field wrapped.
    :param token: unique token to render unique id.
    :param title: title to display.

    """

    def __init__(
        self,
        typ: Type[Any],
        route_prefix: str,
        name: str,
        token: str,
        title: str | None = None,
    ):
        self.typ = typ
        self.route_prefix = route_prefix
        self.name = name
        self.title = title or get_title(typ)
        self.token = token

    @property
    def fullname(self) -> str:
        """Full name for the type."""
        return _get_fullname(self.typ)

    @property
    def id(self) -> str:
        """Unique id to inject in the DOM."""
        name = self.name.replace("_", "-").replace(".", "-").replace(":", "-")
        typ = self.typ.__name__.replace("_", "-")
        return f"{name}-{typ}-{self.token}"

    @property
    def params(self) -> Mapping[str, str]:
        """Params for the widget to render."""
        return {"name": self.name, "token": self.token, "title": self.title}

    @property
    def url(self) -> str:
        """Url to fetch the widget."""
        ret = f"{self.route_prefix}/pydantic-form/widgets/{self.fullname}"
        return ret
