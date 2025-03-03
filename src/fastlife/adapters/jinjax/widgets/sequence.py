from collections.abc import Sequence
from typing import Any

from markupsafe import Markup
from pydantic import Field

from fastlife.service.templates import AbstractTemplateRenderer

from .base import TWidget, TypeWrapper, Widget


class SequenceWidget(Widget[Sequence[TWidget]]):
    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <Details :id="id">
        <Summary :id="id + '-summary'">
          <H3 :class="H3_SUMMARY_CLASS">{{title}}</H3>
          <pydantic_form.Error :text="error" />
        </Summary>
        <div>
          {% set fnGetName = "get" + id.replace("-", "_") %}
          <script>
            function {{ fnGetName }} () {
              const el = document.getElementById("{{id}}-content");
              const len = el.dataset.length;
              el.dataset.length = parseInt(len) + 1;
              return "{{wrapped_type.name}}." + len;
            }
          </script>

          <div id="{{id}}-content" class="m-4"
            data-length="{{children_widgets|length|string}}">
            {% set container_id = id + "-children-container" %}
            <div id="{{container_id}}">
              {% for child in children_widgets %}
              {{ child }}
              {% endfor%}
            </div>
          </div>

          <div>
            {% set container_id = "#" + id + "-children-container" %}
            {% set add_id = id + "-add" %}
            {% set vals = 'js:{"name": '
                + fnGetName
                + '(), "token": "'
                + wrapped_type.token + '", "removable": true}' %}
            <Button type="button"
                :hx-target="container_id" hx-swap="beforeend"
                :id="add_id"
                :hx-vals="vals"
                :hx-get="wrapped_type.url">
              Add
            </Button>
          </div>
        </div>
      </Details>
    </pydantic_form.Widget>
    """

    item_type: type[Any]
    wrapped_type: TypeWrapper | None = Field(default=None)
    children_widgets: list[str] | None = Field(default=None)

    def build_item_type(self, route_prefix: str) -> TypeWrapper:
        return TypeWrapper(self.item_type, route_prefix, self.name, self.token)

    def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version."""
        self.wrapped_type = self.build_item_type(renderer.route_prefix)
        self.children_widgets = [
            Markup(item.to_html(renderer)) for item in self.value or []
        ]
        return Markup(renderer.render_template(self))
