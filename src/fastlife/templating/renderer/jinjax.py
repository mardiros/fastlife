from typing import TYPE_CHECKING, Any, Mapping, MutableMapping, Optional, Sequence, Type

from fastapi import Request
from jinjax.catalog import Catalog
from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife.request.model_result import ModelResult
from fastlife.templating.renderer.widgets.factory import WidgetFactory

if TYPE_CHECKING:
    from fastlife.configurator.settings import Settings  # coverage: ignore

from fastlife.shared_utils.resolver import resolve_path

from .abstract import AbstractTemplateRenderer, AbstractTemplateRendererFactory


def build_searchpath(template_search_path: str) -> Sequence[str]:
    searchpath: list[str] = []
    paths = template_search_path.split(",")

    for path in paths:
        if ":" in path:
            searchpath.append(resolve_path(path))
        else:
            searchpath.append(path)
    return searchpath


class JinjaxRenderer(AbstractTemplateRenderer):
    def __init__(
        self,
        catalog: Catalog,
        request: Request,
        csrf_token_name: str,
        form_data_model_prefix: str,
        route_prefix: str,
    ):
        self.route_prefix = route_prefix
        self.catalog = catalog
        self.request = request
        self.csrf_token_name = csrf_token_name
        self.form_data_model_prefix = form_data_model_prefix
        self.globals: MutableMapping[str, Any] = {}

    def build_globals(self) -> Mapping[str, Any]:
        return {
            "request": self.request,
            "csrf_token": {
                "name": self.csrf_token_name,
                "value": self.request.scope.get(self.csrf_token_name, ""),
            },
            "pydantic_form": self.pydantic_form,
            **self.globals,
        }

    def render_template(
        self,
        template: str,
        *,
        globals: Optional[Mapping[str, Any]] = None,
        **params: Any,
    ) -> str:
        if globals:
            self.globals.update(globals)
        return self.catalog.render(  # type: ignore
            template, __globals=self.build_globals(), **params
        )

    def pydantic_form(
        self,
        model: ModelResult[Any],
        *,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        return WidgetFactory(self, token).get_markup(
            model,
            removable=removable,
            field=field,
        )

    def pydantic_form_field(
        self,
        model: Type[Any],
        *,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        return (
            WidgetFactory(self, token)
            .get_widget(
                model,
                form_data={},
                form_errors={},
                prefix=(name or self.form_data_model_prefix),
                removable=removable,
                field=field,
            )
            .to_html(self)
        )


class JinjaxTemplateRenderer(AbstractTemplateRendererFactory):
    route_prefix: str
    """Used to prefix url to fetch fast life widgets."""

    def __init__(self, settings: "Settings") -> None:
        self.route_prefix = settings.fastlife_route_prefix
        self.form_data_model_prefix = settings.form_data_model_prefix
        self.csrf_token_name = settings.csrf_token_name

        self.catalog = Catalog(
            use_cache=settings.jinjax_use_cache,
            auto_reload=settings.jinjax_auto_reload,
        )
        for path in build_searchpath(settings.template_search_path):
            self.catalog.add_folder(path)

    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        return JinjaxRenderer(
            self.catalog,
            request,
            self.csrf_token_name,
            self.form_data_model_prefix,
            self.route_prefix,
        )
