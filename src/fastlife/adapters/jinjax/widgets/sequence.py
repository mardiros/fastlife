from typing import Any, Sequence, Type

from markupsafe import Markup

from fastlife.services.templates import AbstractTemplateRenderer

from .base import TypeWrapper, Widget


class SequenceWidget(Widget[Sequence[Widget[Any]]]):
    def __init__(
        self,
        name: str,
        *,
        title: str | None,
        hint: str | None = None,
        aria_label: str | None = None,
        value: Sequence[Widget[Any]] | None,
        error: str | None = None,
        item_type: Type[Any],
        token: str,
        removable: bool,
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
        self.item_type = item_type

    def get_template(self) -> str:
        return "pydantic_form.Sequence.jinja"

    def build_item_type(self, route_prefix: str) -> TypeWrapper:
        return TypeWrapper(self.item_type, route_prefix, self.name, self.token)

    def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version."""
        children = [Markup(item.to_html(renderer)) for item in self.value or []]
        return Markup(
            renderer.render_template(
                self.get_template(),
                widget=self,
                type=self.build_item_type(renderer.route_prefix),
                children_widgets=children,
            )
        )
