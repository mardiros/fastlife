"""
Widget for field of type Union.
"""

from collections.abc import Sequence
from typing import Union

from markupsafe import Markup
from pydantic import BaseModel, Field

from fastlife.service.templates import AbstractTemplateRenderer

from .base import TWidget, TypeWrapper, Widget


class UnionWidget(Widget[TWidget]):
    """
    Widget for union types.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div id={id}>
        <Details>
          <Summary id={id + '-union-summary'}>
            <H3 class={globals.H3_SUMMARY_CLASS}>{ globals.gettext(title) }</H3>
            <OptionalErrorText text={error} />
          </Summary>
          <div hx-sync="this" id={"id" + child}>
            {
              if child {
                child
              }
              else {
                for typ in types {
                  <Button type="button"
                    hx-target="closest div"
                    hx-get={typ.url}
                    hx-vals={typ.params}
                    id={typ.id}
                    onclick={"document.getElementById('" + id + "-remove-btn').hidden=false"}
                    class={globals.SECONDARY_BUTTON_CLASS}>{globals.gettext(typ.title)}</Button>
                }
              }
            }
          </div>
          <Button type="button" id={id + '-remove-btn'} hx-target={'#' + id}
            hx-vals={parent_type.params} hx-get={parent_type.url} hidden={not child}
            class={globals.SECONDARY_BUTTON_CLASS}>
            Remove
          </Button>
        </Details>
      </div>
    </Widget>
    """

    children_types: Sequence[type[BaseModel]]
    parent_type: TypeWrapper | None = Field(default=None)

    types: Sequence[TypeWrapper] | None = Field(default=None)
    child: str = Field(default="")

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        """Wrap types in the union in order to get the in their own widgets."""
        return [
            TypeWrapper(typ, route_prefix, self.name, self.token)
            for typ in self.children_types
        ]

    def to_html(self, renderer: "AbstractTemplateRenderer") -> Markup:
        """Return the html version."""
        self.child = Markup(self.value.to_html(renderer)) if self.value else ""
        self.types = self.build_types(renderer.route_prefix)
        self.parent_type = TypeWrapper(
            Union[tuple(self.children_types)],  # type: ignore # noqa: UP007
            renderer.route_prefix,
            self.name,
            self.token,
            title=self.title,
        )
        return Markup(renderer.render_template(self))
