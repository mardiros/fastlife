"""Pydantic models"""

from collections.abc import Sequence

from markupsafe import Markup
from pydantic import Field

from fastlife.service.templates import AbstractTemplateRenderer

from .base import TWidget, Widget


class ModelWidget(Widget[Sequence[TWidget]]):
    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
    <div id="{{id}}"{% if nested %} class="m-4"{%endif%}>
        {% if nested %}
        <Details>
        <Summary :id="id + '-summary'">
            <H3 :class="H3_SUMMARY_CLASS">{{title}}</H3>
            <pydantic_form.Error :text="error" />
        </Summary>
        <div>
            {% for child in children_widgets %}
            {{ child }}
            {% endfor %}
        </div>
        </Details>
        {% else %}
            {% for child in children_widgets %}
            {{ child }}
            {% endfor %}
        {% endif %}
    </div>
    </pydantic_form.Widget>
    """

    nested: bool = Field(default=False)
    children_widgets: list[str] | None = Field(default=None)

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version."""
        self.children_widgets = [child.to_html(renderer) for child in self.value or []]
        return Markup(renderer.render_template(self))
