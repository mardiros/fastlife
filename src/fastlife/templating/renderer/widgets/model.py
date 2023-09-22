from typing import Sequence

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget


class ModelWidget(Widget):
    def __init__(self, name: str, *, title: str, children_widget: Sequence[Widget]):
        super().__init__(name, title)
        self.children_widget = children_widget

    def get_template(self) -> str:
        return "pydantic_form/model.jinja2"

    async def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version"""
        children_widget = [
            await child.to_html(renderer) for child in self.children_widget
        ]
        return Markup(
            await renderer.render_template(
                self.get_template(), widget=self, children_widget=children_widget
            )
        )
