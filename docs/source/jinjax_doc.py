import ast
import re
from pathlib import Path
from typing import Any, cast

from docutils import nodes
from jinjax import InvalidArgument
from sphinx.addnodes import desc_signature
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole

from fastlife.config.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer


class JinjaxComponent(ObjectDescription[str]):
    """Description of a Jinjax component."""

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        node = self.env.get_domain("jinjax").get_full_qualified_name(sig)
        if node:
            signode.append(node)
        return sig

    def add_target_and_index(self, name, sig, signode):
        """Add anchor for references and indexing."""
        targetname = f"jinjax.{name}"
        signode["names"].append(targetname)
        self.state.document.note_explicit_target(signode)
        self.env.domaindata["jinjax"]["components"][name] = self.env.docname

    def run(self):
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
        try:
            astree = ast.parse(signature)
        except SyntaxError as err:
            raise InvalidArgument(f"SyntaxError {err} in \n{signature}") from err
        func_def = cast(ast.FunctionDef, astree.body[0])

        # Create a colorized signature line with separate spans for each part
        signature_node = nodes.literal(classes=["jinjax-signature"])
        signature_node += nodes.inline(text="<")
        signature_node += nodes.inline(
            text=component_name, classes=["jinjax-component-name"]
        )

        def process_arg(arg: ast.arg, default_value: Any, signature_node: Any):
            arg_name = arg.arg.replace("_", "-")
            arg_type = ast.unparse(arg.annotation) if arg.annotation else "Any"

            signature_node += nodes.inline(text=" ")
            signature_node += nodes.inline(text=arg_name, classes=["jinjax-arg"])
            signature_node += nodes.inline(text=": ")
            signature_node += nodes.inline(text=arg_type, classes=["jinjax-type"])
            if default_value is not None:
                signature_node += nodes.inline(text=" = ")
                signature_node += nodes.inline(
                    text=ast.unparse(default_value), classes=["jinjax-default"]
                )

        # Process keyword-only arguments
        kwonlyargs = func_def.args.kwonlyargs
        kw_defaults = func_def.args.kw_defaults

        has_content = False
        for arg, default in zip(kwonlyargs, kw_defaults):
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

        # Add the component description (self.content[0] is the first line of content)
        description = self.content[0] if self.content else "-"
        if description != "-":
            description_node = nodes.paragraph("", description)
            container_node += description_node

        # Handle the parameters (e.g., :param)
        param_list = nodes.definition_list()
        for i in range(1, len(self.content)):
            content_line = self.content[i]
            if content_line.startswith(":param "):
                param_info = content_line[len(":param ") :].split(":", 1)
                param_name = param_info[0].strip()
                param_description = param_info[1].strip() if len(param_info) > 1 else ""

                # Create param definition entry
                term_node = nodes.term("", "", nodes.strong(text=param_name))
                definition_node = nodes.definition(
                    "", nodes.paragraph("", param_description)
                )
                param_list += nodes.definition_list_item("", term_node, definition_node)

        container_node += param_list

        return [container_node]


class JinjaxDomain(Domain):
    """Custom domain for Jinjax components."""

    name = "jinjax"
    label = "Jinjax"
    roles = {
        "component": XRefRole(),
    }
    directives = {
        "component": JinjaxComponent,
    }
    object_types = {
        "component": ObjType("component", "component"),
    }


def run_autodoc(app: Sphinx) -> str | None:
    """Run autodoc for a single package.

    :return: The top level module name, relative to the api directory.
    """
    renderer = JinjaxTemplateRenderer(Settings())
    outdir = Path(app.srcdir) / app.config.jinjax_doc_output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    toctree = ""
    for component in renderer.catalog.iter_components(
        ignores=[re.compile(r"icons..*..*")]
    ):
        outfile = outdir / f"{component.name}.rst"

        outfile.write_text(
            f"{component.name}\n"
            f"{'=' * len(component.name)}\n"
            f"\n{component.build_docstring()}"
        )
        toctree += f"   {component.name}\n"

    outfile = outdir / "index.rst"
    outfile.write_text(INDEX_TPL.format(toctree=toctree))


INDEX_TPL = """\

JinjaX Components
=================

fastlife comes with a set of compoments:

.. toctree::
   :titlesonly:

{toctree}
"""


def setup(app: Sphinx):
    app.add_config_value("jinjax_doc_index_template", INDEX_TPL, "env")
    app.add_config_value("jinjax_doc_output_dir", "components", "env")
    app.add_domain(JinjaxDomain)
    app.connect("builder-inited", run_autodoc)
