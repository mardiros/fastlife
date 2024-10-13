"""
Template rending based on JinjaX.
"""

import logging
import re
from collections.abc import Iterator, Sequence

from jinja2.exceptions import TemplateSyntaxError
from jinjax import DuplicateDefDeclaration, InvalidArgument
from jinjax.catalog import Catalog

from .inspectable_component import InspectableComponent

log = logging.getLogger(__name__)


def to_include(
    name: str,
    ignores: Sequence[re.Pattern[str]] | None = None,
    includes: Sequence[re.Pattern[str]] | None = None,
) -> bool:
    if includes and not any(include.match(name) for include in includes):
        return False

    if ignores and any(ignore.match(name) for ignore in ignores):
        return False

    return True


class InspectableCatalog(Catalog):
    """
    JinjaX Catalog with introspection support.

    Override the catalog in order to iterate over components to build the doc.
    """

    def iter_components(
        self,
        ignores: Sequence[re.Pattern[str]] | None = None,
        includes: Sequence[re.Pattern[str]] | None = None,
    ) -> Iterator[InspectableComponent]:
        """
        Walk into every templates from the settings, iterate over components.

        :params ignores: filter components using an block list.
        :params includes: filter components using an allowed list.
        """
        for prefix, loader in self.prefixes.items():
            for t in loader.list_templates():
                name, file_ext = t.split(".", maxsplit=1)
                name = name.replace("/", ".")
                path, tmpl_name = self._get_component_path(
                    prefix, name, file_ext=file_ext
                )
                is_included = to_include(name, ignores, includes)
                if is_included:
                    try:
                        component = InspectableComponent(
                            name=name, prefix=prefix, path=path, source=path.read_text()
                        )
                    except InvalidArgument as exc:
                        log.error(f"Definition Syntax Error in <{name}/>: {exc}")
                        log.error(path.read_text())
                        continue
                    except DuplicateDefDeclaration as exc:
                        log.error(f"Duplicate Definition in <{name}/>: {exc}")
                        log.error(path.read_text())
                        continue

                    self.jinja_env.loader = loader

                    try:
                        component.tmpl = self.jinja_env.get_template(
                            tmpl_name, globals=self._tmpl_globals
                        )
                    except TemplateSyntaxError as exc:
                        log.error(
                            f"Template Syntax Error in <{name}/>: {exc} on "
                            "{exc.lineno} :"
                        )
                        log.error(path.read_text())
                        continue
                    yield component
