"""
Widget for field of type Union.
"""

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Union

from markupsafe import Markup
from pydantic import BaseModel, Field

from fastlife.domain.model.template import XTemplate

if TYPE_CHECKING:
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
          <div hx-sync="this" id={id + "-child"} class="flex flex-row gap-2 mt-2">
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
          <div class="ml-4 my-2">
            <Button
                type="button"
                id={id + '-remove-btn'}
                hidden={not child}
                class={globals.SECONDARY_BUTTON_CLASS}
                onclick={'resetUnion("' + id + '")'}
                >
                {globals.gettext("Remove")}
            </Button>
            <script>
                function resetUnion(id) {
                    const child = document.getElementById(id + "-child");
                    const defaultBtns = document.getElementById(id + "-default-buttons");
                    const btn = document.getElementById(id + '-remove-btn');
                    child.innerHTML = defaultBtns.innerHTML;
                    btn.hidden = true;
                    htmx.process(child);
                }
            </script>
          </div>
          <div class="hidden" id={id + "-default-buttons"}>
            {
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
          </div>
        </Details>
      </div>
    </Widget>
    """

    children_types: Mapping[str, type[BaseModel]]
    parent_type: TypeWrapper | None = Field(default=None)

    types: Sequence[TypeWrapper] | None = Field(default=None)
    child: str = Field(default="")

    def build_types(self, route_prefix: str) -> Sequence[TypeWrapper]:
        """Wrap types in the union in order to get the in their own widgets."""
        return [
            TypeWrapper(typ, route_prefix, self.name, self.token, title)
            for title, typ in self.children_types.items()
        ]

    def to_html(self, renderer: "AbstractTemplateRenderer[XTemplate]") -> Markup:
        """Return the html version."""
        self.child = Markup(self.value.to_html(renderer)) if self.value else ""
        self.types = self.build_types(renderer.route_prefix)

        self.parent_type = TypeWrapper(
            Union[tuple(self.children_types.values())],  # type: ignore # noqa: UP007
            renderer.route_prefix,
            self.name,
            self.token,
            title=self.title,
        )
        return Markup(renderer.render_template(self))
