import ast
import re
from pathlib import Path
from typing import Any, ClassVar, cast

from docutils import nodes
from sphinx.addnodes import index, pending_xref
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util import relative_uri  # type: ignore

from fastlife.adapters.jinjax.renderer import JinjaxEngine
from fastlife.settings import Settings


def create_ref_node(arg_type: str) -> nodes.Node:
    """
    Creates a cross-reference node if a type has been inferred.

    At the monent, type inferred are types containing a `.`, otherwise
    considered as a simple type from the python standard library.

    This function is used to create links in component parameters.

    :param arg_type: type to render.
    """
    if "|" in arg_type:
        typs = [t.strip() for t in arg_type.split("|")]
        typs_group = nodes.literal()
        for idx, typ in enumerate(typs):
            if idx:
                typs_group += nodes.Text(" | ")
            typs_group += create_ref_node(typ)
        return typs_group

    if "." in arg_type:
        ref_node = pending_xref(
            "",
            refdomain="py",
            reftype="class",
            reftarget=arg_type,
            refexplicit=True,
            refwarn=True,
            classes=[],
        )
        ref_node += nodes.Text(arg_type)
        return ref_node
    else:
        return nodes.inline(text=arg_type, classes=["jinjax-type"])


def handle_arg_type(arg_type: str, signature_node: nodes.literal) -> None:
    """Add arg_type to signature_node."""
    complex_type_pattern = r"(\w+)\[(.+)\]"

    match = re.match(complex_type_pattern, arg_type)
    if match:
        outer_type, inner_type = match.groups()
        signature_node += nodes.inline(text=f"{outer_type}[", classes=["jinjax-type"])
        signature_node += create_ref_node(inner_type)
        signature_node += nodes.inline(text="]", classes=["jinjax-type"])
    else:
        signature_node += create_ref_node(arg_type)


class JinjaxComponent(ObjectDescription[str]):
    """Description of a Jinjax component."""

    def run(self) -> list[nodes.Node]:
        """Generate structured and styled documentation for the directive."""
        container_node = nodes.container(classes=["jinjax-component"])

        # Extract the signature (first line of arguments)
        signature_text = self.arguments[0]
        component_name, rest = signature_text.split("(", 1)

        params = rest.rstrip(")")
        if params:
            signature = f"def component(*, {params}): pass"
        else:
            # no parameters in the component
            signature = "def component(): pass"

        astree = ast.parse(signature)
        func_def = cast(ast.FunctionDef, astree.body[0])

        # Create a colorized signature line with separate spans for each part
        signature_node = nodes.literal(classes=["jinjax-signature"])
        signature_node += nodes.inline(text="<")
        signature_node += nodes.inline(
            text=component_name, classes=["jinjax-component-name"]
        )

        def process_arg(arg: ast.arg, default_value: Any, signature_node: Any) -> None:
            arg_name = arg.arg.replace("_", "-").rstrip("-")
            arg_type = ast.unparse(arg.annotation) if arg.annotation else "Any"
            signature_node += nodes.inline(text=" ")

            signature_node += nodes.inline(text=arg_name, classes=["jinjax-arg"])
            signature_node += nodes.inline(text=": ")

            handle_arg_type(arg_type, signature_node)

            if default_value is not None:
                signature_node += nodes.inline(text=" = ")
                signature_node += nodes.inline(
                    text=ast.unparse(default_value), classes=["jinjax-default"]
                )

        # Process keyword-only arguments
        kwonlyargs = func_def.args.kwonlyargs
        kw_defaults = func_def.args.kw_defaults

        has_content = False
        for arg, default in zip(kwonlyargs, kw_defaults, strict=False):
            if arg.arg == "content":
                has_content = True
            else:
                process_arg(arg, default, signature_node)

        signature_close_wrapper = nodes.container(classes=["jinjax-signature-close"])
        if has_content:
            signature_node += nodes.inline(text=">")
            signature_node += nodes.inline(
                text="{{- content -}}", classes=["jinjax-child-content"]
            )
            signature_close_wrapper += nodes.inline(text="</")
            signature_close_wrapper += nodes.inline(
                text=component_name, classes=["jinjax-component-name"]
            )
            signature_close_wrapper += nodes.inline(text=">")
        else:
            signature_node += nodes.inline(text=" />")
            signature_close_wrapper += nodes.inline(text="")
        signature_node += signature_close_wrapper

        signature_node_wrapper = nodes.container(classes=["jinjax-signature-wrapper"])
        signature_node_wrapper += signature_node

        container_node += nodes.paragraph("", "", signature_node_wrapper)

        if self.content:
            content = self.parse_content_to_nodes(allow_section_headings=True)
            for content_node in content:
                container_node += content_node

        index_entry = index(
            entries=[
                (
                    "single",
                    f"{component_name} (JinjaX component)",
                    f"jinjax-component-{component_name}",
                    "",
                    None,
                )
            ]
        )
        return [index_entry, container_node]


class JinjaxDomain(Domain):
    """Custom domain for Jinjax components."""

    name = "jinjax"
    label = "Jinjax"
    roles = {  # noqa: RUF012
        "component": XRefRole(),
    }
    directives = {  # noqa: RUF012
        "component": JinjaxComponent,
    }
    object_types = {  # noqa: RUF012
        "component": ObjType("component", "component"),
    }

    _components: ClassVar[list[str]] = []

    @classmethod
    def register(cls, component: str) -> None:
        cls._components.append(component)

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: nodes.Element,
    ) -> nodes.Element | None:
        """Resolve the pending_xref *node* with the given *typ* and *target*.

        This method should return a new node, to replace the xref node,
        containing the *contnode* which is the markup content of the
        cross-reference.

        If no resolution can be found, None can be returned; the xref node will
        then given to the :event:`missing-reference` event, and if that yields no
        resolution, replaced by *contnode*.

        The method can also raise :exc:`sphinx.environment.NoUri` to suppress
        the :event:`missing-reference` event being emitted.
        """
        ret = self.resolve_any_xref(env, fromdocname, builder, target, node, contnode)
        return ret[0][1] if ret else None

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: nodes.Element,
    ) -> list[tuple[str, nodes.Element]]:
        """Resolve the pending_xref *node* with the given *target*.

        The reference comes from an "any" or similar role, which means that we
        don't know the type.  Otherwise, the arguments are the same as for
        {meth}`JinjaxDomain.resolve_xref`.

        The method must return a list (potentially empty) of tuples
        ``('domain:role', newnode)``, where ``'domain:role'`` is the name of a
        role that could have created the same reference, e.g. ``'py:func'``.
        ``newnode`` is what {meth}`JinjaxDomain.resolve_xref` would return.

        .. versionadded:: 1.3
        """
        if target in self._components:
            ref_uri = f"components/{target}.html"
            relative_link = relative_uri(fromdocname, ref_uri)

            if isinstance(contnode, nodes.literal) and contnode.astext() == target:
                contnode = nodes.literal("", f"<{target}/>")

            newnode = nodes.reference("", "", contnode, refuri=relative_link)
            return [("jinjax:component", newnode)]

        return []


def run_autodoc(app: Sphinx) -> None:
    """Run autodoc for a single package.

    :return: The top level module name, relative to the api directory.
    """
    renderer = JinjaxEngine(
        Settings(template_search_path=app.config.jinjax_template_search_path)
    )
    outdir = Path(app.srcdir) / app.config.jinjax_doc_output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    toctree = ""

    ignores = [re.compile(rx) for rx in app.config.jinjax_ignores_pattern.split(",")]

    for component in renderer.catalog.iter_components(ignores=ignores):
        outfile = outdir / f"{component.name}.rst"

        outfile.write_text(
            f"{component.name}\n"
            f"{'=' * len(component.name)}\n"
            f"\n{component.build_docstring()}"
        )
        toctree += f"   {component.name}\n"
        JinjaxDomain.register(component.name)

    outfile = outdir / "index.rst"
    outfile.write_text(INDEX_TPL.format(toctree=toctree))


INDEX_TPL = """\

.. _jinjax-components:

JinjaX Components
=================

fastlife comes with a set of compoments:

.. toctree::
   :titlesonly:

{toctree}
"""


def setup(app: Sphinx) -> None:
    app.add_config_value("jinjax_doc_index_template", INDEX_TPL, "env")
    app.add_config_value("jinjax_doc_output_dir", "components", "env")
    app.add_config_value("jinjax_template_search_path", "fastlife:components", "env")
    app.add_config_value("jinjax_ignores_pattern", r"^icons\..*", "env")
    app.add_domain(JinjaxDomain)
    app.connect("builder-inited", run_autodoc)
