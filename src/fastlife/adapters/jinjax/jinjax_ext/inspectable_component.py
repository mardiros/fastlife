"""
Template rending based on JinjaX.
"""

import ast
import logging
import re
from pathlib import Path
from typing import cast

from jinja2 import Template
from jinjax.component import RX_ARGS_START, RX_META_HEADER, Component

from .docstring import generate_docstring

log = logging.getLogger(__name__)

RX_DOC_START = re.compile(r"{#-?\s*doc\s+")
RX_CONTENT = re.compile(r"\{\{-?\s*content\s*-?\}\}", re.DOTALL)
RX_COMMENT_REPLACE = re.compile(r"{#[^#]+#}")


SIGNATURE = """
def component({args}):
    '''
    {docstring}
    '''
    ...
"""


def has_content(source: str) -> bool:
    nocomment = RX_COMMENT_REPLACE.sub("", source)
    return len(RX_CONTENT.findall(nocomment)) > 0


class InspectableComponent(Component):
    """
    JinjaX Components override that support intropspection.

    The Component class of JinjaX does not support documentation by default.
    """

    __slots__ = (
        "css",
        "js",
        "mtime",
        "name",
        "optional",
        "path",
        "prefix",
        "required",
        "source",
        "tmpl",
        "url_prefix",
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
        """Return the component definition as a python function definition."""
        signature = "def component(): pass"
        match = RX_META_HEADER.match(self.source)
        if match:
            headers = match.group(0)
            header = headers.split("#}")[:-1]
            docstring = ""

            expr = None
            while header:
                item = header.pop(0).strip(" -\n")

                expr = self.read_metadata_item(item, RX_ARGS_START)  # type: ignore
                doc = self.read_metadata_item(item, RX_DOC_START)  # type: ignore
                if doc:
                    docstring += f"    {doc.strip()}\n"
                    continue

            sigargs = f"*, {expr}" if expr else ""
            signature = SIGNATURE.format(args=sigargs, docstring=docstring or "")

        astree = ast.parse(signature)
        return cast(ast.FunctionDef, astree.body[0])

    def build_docstring(self) -> str:
        """Build a rst docstring for the jinjax component."""
        func_def = self.as_def()
        prefix = f"{self.prefix}." if self.prefix else ""
        ret = ".. jinjax:component:: " + generate_docstring(
            func_def, f"{prefix}{self.name}", has_content(self.source)
        )
        return ret
