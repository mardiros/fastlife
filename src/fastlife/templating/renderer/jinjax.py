from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence, Type

from fastapi import Request
from jinjax.catalog import Catalog
from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife.templating.renderer.widgets.factory import WidgetFactory

if TYPE_CHECKING:
    from fastlife.configurator.settings import Settings

from fastlife.shared_utils.resolver import resolve_path

from .abstract import AbstractTemplateRenderer


def build_searchpath(template_search_path: str) -> Sequence[str]:
    searchpath: list[str] = []
    paths = template_search_path.split(",")

    for path in paths:
        if ":" in path:
            searchpath.append(resolve_path(path))
        else:
            searchpath.append(path)
    return searchpath


class JinjaxTemplateRenderer(AbstractTemplateRenderer):
    route_prefix: str
    """Used to prefix url to fetch fast life widgets."""

    def __init__(self, settings: "Settings") -> None:
        self.route_prefix = settings.fastlife_route_prefix
        self.form_data_model_prefix = settings.form_data_model_prefix
        self.csrf_token_name = settings.csrf_token_name

        self.catalog = Catalog()
        for path in build_searchpath(settings.template_search_path):
            self.catalog.add_folder(path)

    def render_page(self, request: Request, template: str, **params: Any) -> str:
        return self.catalog.render(  # type:ignore
            template,
            request=request,
            csrf_token={
                "name": self.csrf_token_name,
                "value": request.scope.get(self.csrf_token_name, ""),
            },
            pydantic_form=self.pydantic_form,
            **params
        )

    def render_template(self, template: str, **params: Any) -> str:
        return self.catalog.render(template, **params)  # type:ignore

    def pydantic_form(
        self,
        model: Type[Any],
        form_data: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        return WidgetFactory(self, token).get_markup(
            model,
            form_data or {},
            prefix=(name or self.form_data_model_prefix),
            removable=removable,
            field=field,
        )
