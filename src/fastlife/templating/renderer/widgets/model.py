from typing import Any, Sequence

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

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
        token: str,
    ):
        super().__init__(
            name,
            title=title,
            value=value,
            error=error,
            removable=removable,
            token=token,
        )

    def get_template(self) -> str:
        return "pydantic_form.Model"

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version"""
        children_widget = [child.to_html(renderer) for child in self.value or []]
        kwargs = {
            "widget": self,
            "children_widget": children_widget,
        }
        return Markup(
            renderer.render_template(self.get_template(), globals=None, **kwargs)
        )
