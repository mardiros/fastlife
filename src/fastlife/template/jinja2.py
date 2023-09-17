from pathlib import Path
from typing import Any, Sequence
from .renderer import AbstractTemplateRenderer

from jinja2 import Environment, FileSystemLoader


import importlib.util


def build_searchpath(template_search_path: str) -> Sequence[str]:
    searchpath: list[str] = []
    paths = template_search_path.split(",")

    for path in paths:
        if ":" in path:
            package_name, resource_name = path.split(":", 1)
            spec = importlib.util.find_spec(package_name)
            if spec:
                package_path = spec.origin
                if not package_path:
                    raise ValueError(f"{path} not found")
                full_path = Path(package_path).parent / resource_name
                searchpath.append(str(full_path))
        else:
            searchpath.append(path)
    return searchpath


class Jinja2TemplateRenderer(AbstractTemplateRenderer):
    def __init__(self, template_search_path: str) -> None:
        super().__init__()
        self.env = Environment(
            loader=FileSystemLoader(build_searchpath(template_search_path)),
            enable_async=True,
        )

    async def render_template(self, template: str, **kwargs: Any) -> str:
        tpl = self.env.get_template(template)
        ret = await tpl.render_async(**kwargs)
        return ret
