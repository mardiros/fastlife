"""Pydantic models"""

from collections.abc import Sequence

from markupsafe import Markup
from pydantic import Field

from fastlife.service.templates import AbstractTemplateRenderer

from .base import TWidget, Widget


class ModelWidget(Widget[Sequence[TWidget]]):
    template = """
    <Widget widget_id={id} removable={removable}>
    <div id={id} class={if nested {"m-4"}}>
        {
          if nested {
            <Details>
              <Summary id={id + '-summary'}>
                <H3 class={globals.H3_SUMMARY_CLASS}>{ globals.gettext(title) }</H3>
                <OptionalErrorText text={error} />
              </Summary>
              <div>
                {
                  for child in children_widgets {
                    child
                  }
                }
              </div>
            </Details>
          }
          else {
            for child in children_widgets {
              child
            }
          }
        }
    </div>
    </Widget>
    """

    nested: bool = Field(default=False)
    children_widgets: list[str] | None = Field(default=None)

    def to_html(self, renderer: AbstractTemplateRenderer) -> Markup:
        """Return the html version."""
        self.children_widgets = [child.to_html(renderer) for child in self.value or []]
        return Markup(renderer.render_template(self))
