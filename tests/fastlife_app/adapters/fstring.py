"""Render template using templates containing python f-string like format."""

from pathlib import Path

from fastlife import Configurator, Request, configure
from fastlife.domain.model.template import InlineTemplate
from fastlife.service.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)

templates = Path(__file__).parent / "templates"


class FStringTemplateRenderer(AbstractTemplateRenderer):
    def render_template(self, template: InlineTemplate) -> str:
        return template.template.format(**template.model_dump())


class FStringTemplateRendererFactory(AbstractTemplateRendererFactory):
    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        return FStringTemplateRenderer(request)


@configure
def includeme(conf: Configurator) -> None:
    conf.add_renderer(".fstring", FStringTemplateRendererFactory())
