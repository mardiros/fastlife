from typing import Any, Optional, Sequence, Type

from markupsafe import Markup

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import TypeWrapper, Widget


class SequenceWidget(Widget):
    items: Sequence[Widget]

    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        help_text: Optional[str],
        items: Optional[Sequence[Widget]],
        item_type: Type[Any],
        token: str,
        removable: bool,
    ):
        super().__init__(name, title=title, token=token, removable=removable)
        self.items = items or []
        self.item_type = item_type
        self.help_text = help_text

    def get_template(self) -> str:
        return "pydantic_form/sequence.jinja2"

    def build_item_type(self, route_prefix: str) -> TypeWrapper:
        return TypeWrapper(self.item_type, route_prefix, self.name, self.token)

    async def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version"""
        children = [Markup(await item.to_html(renderer)) for item in self.items]
        return Markup(
            await renderer.render_template(
                self.get_template(),
                widget=self,
                type=self.build_item_type(renderer.route_prefix),
                children_widgets=children,
            )
        )
