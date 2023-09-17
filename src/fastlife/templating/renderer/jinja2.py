from typing import Any, Sequence

from jinja2 import Environment, FileSystemLoader

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
