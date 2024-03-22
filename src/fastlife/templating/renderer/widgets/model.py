from typing import Sequence

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget


class ModelWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        children_widget: Sequence[Widget],
        removable: bool,
        title: str,
        token: str,
    ):
        super().__init__(name, title=title, removable=removable, token=token)
        self.children_widget = children_widget

    def get_template(self) -> str:
        return "pydantic_form.Model"

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version"""
        children_widget = [child.to_html(renderer) for child in self.children_widget]
        kwargs = {
            "widget": self,
            "children_widget": children_widget,
        }
        return Markup(renderer.render_template(self.get_template(), **kwargs))
