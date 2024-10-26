"""Render template using templates containing python f-string like format."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from fastlife import Configurator, Request, configure
from fastlife.services.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)
from fastlife.templates.inline import InlineTemplate

templates = Path(__file__).parent / "templates"


class FStringTemplateRenderer(AbstractTemplateRenderer):
    def render_template(
        self,
        template: str,
        *,
        globals: Mapping[str, Any] | None = None,
        **params: Any,
    ) -> str:
        text = (templates / template).read_text()
        return text.format(**params)

    def render_inline(self, template: InlineTemplate) -> str:
        raise NotImplementedError


class FStringTemplateRendererFactory(AbstractTemplateRendererFactory):
    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        return FStringTemplateRenderer(request)


@configure
def includeme(conf: Configurator) -> None:
    conf.add_renderer(".fstring", FStringTemplateRendererFactory())
