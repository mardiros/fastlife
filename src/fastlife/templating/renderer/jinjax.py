"""Template rending based on JinjaX."""

import ast
import logging
import re
import textwrap
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    cast,
)

from fastapi import Request
from jinja2 import Template
from jinja2.exceptions import TemplateSyntaxError
from jinjax import InvalidArgument
from jinjax.catalog import Catalog
from jinjax.component import RX_ARGS_START, RX_META_HEADER, Component
from jinjax.exceptions import DuplicateDefDeclaration
from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife.request.form import FormModel
from fastlife.templating.renderer.widgets.factory import WidgetFactory

if TYPE_CHECKING:
    from fastlife.config.settings import Settings  # coverage: ignore

from fastlife.shared_utils.resolver import resolve, resolve_path

from .abstract import AbstractTemplateRenderer, AbstractTemplateRendererFactory

log = logging.getLogger(__name__)

RX_DOC_START = re.compile(r"{#-?\s*doc\s+")
RX_CONTENT = re.compile(r"\{\{-?\s*content\s*-?\}\}", re.DOTALL)
RX_COMMENT_REPLACE = re.compile(r"{#[^#]+#}")


def has_content(source: str) -> bool:
    nocomment = RX_COMMENT_REPLACE.sub("", source)
    return len(RX_CONTENT.findall(nocomment)) > 0


def generate_docstring(
    func_def: ast.FunctionDef, component_name: str, add_content: bool
) -> str:
    """Generate a docstring for the component."""
    # Extract function name and docstring
    docstring = (ast.get_docstring(func_def, clean=True) or "").strip()
    if docstring:
        docstring = textwrap.dedent(docstring)
        docstring_lines = [l for l in docstring.split("\n")]
        # Add a newline for separation after the function docstring
        docstring_lines.append("")
    else:
        docstring_lines = []

    component_params: list[str] = []

    # Function for processing an argument and adding its docstring lines
    def process_arg(arg: ast.arg, default_value: Any = None) -> None:
        arg_name = arg.arg
        param_desc = ""
        # Extract the type annotation (if any)
        if (
            isinstance(arg.annotation, ast.Subscript)
            and isinstance(arg.annotation.value, ast.Name)
            and arg.annotation.value.id == "Annotated"
        ):
            # For Annotated types, we expect the first argument to be the type and
            # the second to be the description
            type_annotation = arg.annotation.slice.elts[0]  # type: ignore
            param_type = ast.unparse(type_annotation)

            if len(arg.annotation.slice.elts) > 1 and isinstance(  # type: ignore
                arg.annotation.slice.elts[1],  # type: ignore
                ast.Constant,  # type: ignore
            ):
                param_desc = arg.annotation.slice.elts[1].value  # type: ignore
        else:
            # Otherwise, just use the type if available
            param_type = ast.unparse(arg.annotation) if arg.annotation else "Any"

        # Build the parameter docstring line
        docstring_lines.append(f":param {arg_name.rstrip('_')}: {param_desc}".strip())

        # Build the string representation of the parameter
        param_str = f"{arg_name}: {param_type}"
        if default_value is not None:
            param_str += f" = {ast.unparse(default_value)}"  # type: ignore

        component_params.append(param_str)

    # Process keyword-only arguments
    kwonlyargs = func_def.args.kwonlyargs
    kw_defaults = func_def.args.kw_defaults

    for arg, default in zip(kwonlyargs, kw_defaults):
        process_arg(arg, default)

    if add_content:
        component_params.append("content: Any")
        docstring_lines.append(":param content: child node.")

    return (
        f"{component_name}({', '.join(component_params)})"
        + "\n"
        + "\n    "
        + ("\n    ".join(docstring_lines).strip()).replace("\n    \n", "\n\n")
        + "\n"
    )


class InspectableComponent(Component):
    __slots__ = (
        "name",
        "prefix",
        "url_prefix",
        "required",
        "optional",
        "css",
        "js",
        "path",
        "mtime",
        "tmpl",
        "source",
    )

    def __init__(
        self,
        *,
        name: str,
        prefix: str = "",
        url_prefix: str = "",
        source: str = "",
        mtime: float = 0,
        tmpl: "Template | None" = None,
        path: "Path | None" = None,
    ) -> None:
        super().__init__(
            name=name,
            prefix=prefix,
            url_prefix=url_prefix,
            source=source,
            mtime=mtime,
            tmpl=tmpl,
            path=path,
        )
        self.source = source

    def as_def(self) -> ast.FunctionDef:
        signature = "def component(): pass"
        match = RX_META_HEADER.match(self.source)
        if match:
            headers = match.group(0)
            header = headers.split("#}")[:-1]
            def_found = False
            docstring = ""

            expr = None
            while header:
                item = header.pop(0).strip(" -\n")

                expr = self.read_metadata_item(item, RX_ARGS_START)
                if expr:
                    if def_found:
                        raise DuplicateDefDeclaration(self.name)
                    def_found = True
                    continue

                doc = self.read_metadata_item(item, RX_DOC_START)
                if doc:
                    docstring += f"    {doc.strip()}\n"
                    continue

            if expr:
                signature = f"""\
def component(*, {expr}):
    '''
    {docstring or ""}
    '''
    ...
"""
            elif docstring:
                signature = f"""\
def component():
    '''
    {docstring}
    '''
    ...
"""

        try:
            astree = ast.parse(signature)
        except SyntaxError as err:
            raise InvalidArgument(err) from err
        return cast(ast.FunctionDef, astree.body[0])

    def build_docstring(self) -> str:
        func_def = self.as_def()
        prefix = f"{self.prefix}." if self.prefix else ""
        ret = ".. jinjax:component:: " + generate_docstring(
            func_def, f"{prefix}{self.name}", has_content(self.source)
        )
        return ret


class InspectableCatalog(Catalog):
    """
    Override the catalog in order to iterate over components to build the doc.
    """

    def iter_components(
        self,
        ignores: Sequence[re.Pattern[str]] | None = None,
        includes: Sequence[re.Pattern[str]] | None = None,
    ) -> Iterator[InspectableComponent]:
        for prefix, loader in self.prefixes.items():
            for t in loader.list_templates():
                name, file_ext = t.split(".", maxsplit=1)
                name = name.replace("/", ".")
                path, tmpl_name = self._get_component_path(
                    prefix, name, file_ext=file_ext
                )

                to_include = True
                if includes:
                    to_include = False
                    for include in includes:
                        if include.match(name):
                            to_include = True
                            break
                if to_include and ignores:
                    for ignore in ignores:
                        if ignore.match(name):
                            to_include = False
                            break

                if to_include:
                    component = InspectableComponent(
                        name=name, prefix=prefix, path=path, source=path.read_text()
                    )

                    self.jinja_env.loader = loader
                    try:
                        component.tmpl = self.jinja_env.get_template(
                            tmpl_name, globals=self._tmpl_globals
                        )
                    except TemplateSyntaxError as exc:
                        log.error(f"Syntax Error: {exc} on {exc.lineno} :")
                        log.error(path.read_text())
                        continue
                    yield component


def build_searchpath(template_search_path: str) -> Sequence[str]:
    """
    Build the path containing templates.

    Path may be absolute directories or directories relative to a python
    package. For instance, the `fastlife:templates` is the directory templates
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
        """
        Build globals variables accessible in any templates.

        * `request` is the {class}`current request <fastlife.request.request.Request>`
        * `csrf_token` is used to build for {jinjax:component}`CsrfToken`.
        """
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
        self, model: FormModel[Any], *, token: Optional[str] = None
    ) -> Markup:
        return WidgetFactory(self, token).get_markup(model)

    def pydantic_form_field(
        self,
        model: Type[Any],
        *,
        name: str | None,
        token: str | None,
        removable: bool,
        field: FieldInfo | None,
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
    """
    The default template renderer factory. Based on JinjaX.

    :param settings: setting used to configure jinjax.
    """

    route_prefix: str
    """Used to prefix url to fetch fast life widgets."""

    def __init__(self, settings: "Settings") -> None:
        self.route_prefix = settings.fastlife_route_prefix
        self.form_data_model_prefix = settings.form_data_model_prefix
        self.csrf_token_name = settings.csrf_token_name
        globals = resolve(settings.jinjax_global_catalog_class)().model_dump()

        self.catalog = InspectableCatalog(
            use_cache=settings.jinjax_use_cache,
            auto_reload=settings.jinjax_auto_reload,
            globals=globals,
        )
        for path in build_searchpath(settings.template_search_path):
            self.catalog.add_folder(path)

    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        """Build the renderer to render request for template."""
        return JinjaxRenderer(
            self.catalog,
            request,
            self.csrf_token_name,
            self.form_data_model_prefix,
            self.route_prefix,
        )
