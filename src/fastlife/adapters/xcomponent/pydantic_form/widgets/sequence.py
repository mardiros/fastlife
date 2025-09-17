from collections.abc import Sequence
from typing import Any

from markupsafe import Markup
from pydantic import Field

from fastlife.service.templates import AbstractTemplateRenderer

from .base import TWidget, TypeWrapper, Widget


class SequenceWidget(Widget[Sequence[TWidget]]):
    template = """
    <Widget widget_id={id} removable={removable}>
      <Details id={id}>
        <Summary id={id + '-summary'}>
          <H3 class={globals.H3_SUMMARY_CLASS}>{ globals.gettext(title) }</H3>
          <OptionalErrorText text={error} />
        </Summary>
        <div>
          <script>
            // this function should be added once.
            function getName(name, id) {
              const el = document.getElementById(id + '-content');
              const len = el.dataset.length;
              el.dataset.length = parseInt(len) + 1;
              return name + '.' + len;
            }
          </script>
          <div id={id + "-content"} class="m-4"
            data-length={len(children_widgets)}>
            { let container_id = id + "-children-container" }
            <div id={container_id}>
              {
                for child in children_widgets {
                  child
                }
              }
            </div>
          </div>
          <div>
            { let container_id = "#" + id + "-children-container" }
            { let add_id = id + "-add" }
            { let vals = 'js:{"name": getName("' + wrapped_type.name + '", "' + id + '")'
                + ', "token": "'
                + wrapped_type.token + '", "removable": true}'
            }
            <Button type="button"
                hx-target={container_id} hx-swap="beforeend"
                id={add_id}
                hx-vals={vals}
                hx-get={wrapped_type.url}>
              Add
            </Button>
          </div>
        </div>
      </Details>
    </Widget>
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
