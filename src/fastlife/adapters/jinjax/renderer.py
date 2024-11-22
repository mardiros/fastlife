"""
Template rending based on JinjaX.
"""

import logging
import textwrap
from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    Any,
)

from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife import Request
from fastlife.adapters.fastapi.form import FormModel
from fastlife.adapters.jinjax.widget_factory.factory import WidgetFactory
from fastlife.request.localizer import get_localizer
from fastlife.templates.inline import InlineTemplate

if TYPE_CHECKING:
    from fastlife.settings import Settings  # coverage: ignore

from fastlife.services.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)
from fastlife.shared_utils.resolver import resolve, resolve_path

from .jinjax_ext.inspectable_catalog import InspectableCatalog

log = logging.getLogger(__name__)


def build_searchpath(template_search_path: str) -> Sequence[str]:
    """
    Build the path containing templates.

    Path may be absolute directories or directories relative to a python
    package. For instance, the `fastlife:components` is the directory components
    inside the fastlife installation dir.

    :param template_search_path: list of path separated by a comma (`,`).
    :return: List resolved path.
    """
    searchpath: list[str] = []
    paths = template_search_path.split(",")

    for path in paths:
        if ":" in path:
            searchpath.append(resolve_path(path))
        else:
            searchpath.append(path)
    return searchpath


class JinjaxRenderer(AbstractTemplateRenderer):
    """Render templates using JinjaX."""

    def __init__(
        self,
        catalog: InspectableCatalog,
        request: Request,
    ):
        super().__init__(request)
        self.catalog = catalog
        self.settings = request.registry.settings
        self.translations = get_localizer(request)
        self.globals["pydantic_form"] = self.pydantic_form

    def render_template(self, template: InlineTemplate) -> str:
        """
        Render the JinjaX component with the given parameter.

        :param template: the template to render
        :param globals: parameters that will be used by the JinjaX component and all its
            child components without "props drilling".
        :param params: parameters used to render the template.
        """
        params = template.model_dump()
        src = (
            f"{{# def {', '.join(params.keys())} #}}\n"
            f"{textwrap.dedent(template.template)}"
        )
        return self.catalog.render(
            template.__class__.__qualname__,
            __source=src,
            __globals=self.globals,
            **params,
        )

    def pydantic_form(
        self, model: FormModel[Any], *, token: str | None = None
    ) -> Markup:
        """
        Generate HTML markup to build a form from the given form model.

        :param model: the form model that will be transformed to markup.
        :param token: a token used to ensure that unique identifier are unique.
        :return: HTML Markup generated by composign fields widgets.
        """
        return WidgetFactory(self, token).get_markup(model)

    def pydantic_form_field(
        self,
        model: type[Any],
        *,
        name: str | None,
        token: str | None,
        removable: bool,
        field: FieldInfo | None,
    ) -> Markup:
        """
        Generate HTML for a particular field in a form.

        This function is used to generate union subtypes in Ajax requests.
        :param model: a pydantic or python builtin type that is requests to be rendered
        :param name: name for the field
        :param token: the token of the form to render unique identifiers
        :param removable: add a way let the user remove the widget
        :param field: only render this particular field for the model.
        :return: HTML Markup.
        """
        return (
            WidgetFactory(self, token)
            .get_widget(
                model,
                form_data={},
                form_errors={},
                prefix=(name or self.request.registry.settings.form_data_model_prefix),
                removable=removable,
                field=field,
            )
            .to_html(self)
        )


class JinjaxEngine(AbstractTemplateRendererFactory):
    """
    The default template renderer factory. Based on JinjaX.

    :param settings: setting used to configure jinjax.
    """

    def __init__(self, settings: "Settings") -> None:
        globals = resolve(settings.jinjax_global_catalog_class)().model_dump()

        self.catalog = InspectableCatalog(
            use_cache=settings.jinjax_use_cache,
            file_ext=settings.jinjax_file_ext,
            auto_reload=settings.jinjax_auto_reload,
            globals=globals,
        )
        self.catalog.jinja_env.add_extension("jinja2.ext.i18n")
        for path in build_searchpath(settings.template_search_path):
            self.catalog.add_folder(path)

    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        """Build the renderer to render request for template."""
        return JinjaxRenderer(
            self.catalog,
            request,
        )
