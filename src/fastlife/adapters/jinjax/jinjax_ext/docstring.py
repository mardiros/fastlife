"""
Template rending based on JinjaX.
"""

import ast
import textwrap
from typing import Any


def generate_docstring(
    func_def: ast.FunctionDef, component_name: str, add_content: bool
) -> str:
    """Generate a docstring for a JinjaX component."""
    # Extract function name and docstring
    docstring = (ast.get_docstring(func_def, clean=True) or "").strip()
    if docstring:
        docstring = textwrap.dedent(docstring)
        docstring_lines = [line for line in docstring.split("\n")]
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
            param_type = ast.unparse(type_annotation)  # type: ignore

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

    for arg, default in zip(kwonlyargs, kw_defaults, strict=False):
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
