"""Pydantic models"""

from collections.abc import Sequence
from typing import Any

from markupsafe import Markup

from fastlife.services.templates import AbstractTemplateRenderer

from .base import Widget


class ModelWidget(Widget[Sequence[Widget[Any]]]):
    def __init__(
        self,
        name: str,
        *,
        value: Sequence[Widget[Any]],
        error: str | None = None,
        removable: bool,
        title: str,
        hint: str | None = None,
        aria_label: str | None = None,
        token: str,
        nested: bool,
    ):
        super().__init__(
            name,
            title=title,
            hint=hint,
            aria_label=aria_label,
            value=value,
            error=error,
            removable=removable,
            token=token,
        )
        self.nested = nested

    def get_template(self) -> str:
        return "pydantic_form.Model.jinja"

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version."""
        children_widget = [child.to_html(renderer) for child in self.value or []]
        kwargs = {
            "widget": self,
            "children_widget": children_widget,
        }
        return Markup(
            renderer.render_template(self.get_template(), globals=None, **kwargs)
        )
