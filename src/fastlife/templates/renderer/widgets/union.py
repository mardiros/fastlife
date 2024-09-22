"""
Widget for field of type Union.
"""
from typing import Any, Optional, Sequence, Type, Union

from markupsafe import Markup
from pydantic import BaseModel

from fastlife.services.templates import AbstractTemplateRenderer

from .base import TypeWrapper, Widget


class UnionWidget(Widget[Widget[Any]]):
    """
    Widget for union types.

    :param name: input name.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param value: current value.
    :param error: error of the value if any.
    :param children_types: childrens types list.
    :param removable: display a button to remove the widget for optional fields.
    :param token: token used to get unique id on the form.

    """

    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        hint: Optional[str] = None,
        aria_label: Optional[str] = None,
        value: Optional[Widget[Any]],
        error: str | None = None,
        children_types: Sequence[Type[BaseModel]],
        removable: bool = False,
        token: str,
    ):
        super().__init__(
            name,
            value=value,
            error=error,
            title=title,
            hint=hint,
            aria_label=aria_label,
            token=token,
            removable=removable,
        )
        self.children_types = children_types
        self.parent_name = name

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        """Wrap types in the union in order to get the in their own widgets."""
        return [
            TypeWrapper(typ, route_prefix, self.name, self.token)
            for typ in self.children_types
        ]

    def get_template(self) -> str:
        return "pydantic_form.Union.jinja"

    def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version."""
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
