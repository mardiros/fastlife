from typing import Sequence
from xmlrpc.client import boolean

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget


class ModelWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        children_widget: Sequence[Widget],
        required: boolean,
        title: str,
        token: str,
    ):
        super().__init__(name, title=title, required=required, token=token)
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
