"""Render template using templates containing python f-string like format."""

from pathlib import Path
from typing import Any

from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife import Configurator, Request, configure
from fastlife.adapters.fastapi.form import FormModel
from fastlife.domain.model.template import InlineTemplate
from fastlife.service.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)

templates = Path(__file__).parent / "templates"


class FString(InlineTemplate):
    """Render Fstring"""


class FStringTemplateRenderer(AbstractTemplateRenderer[FString]):
    def render_template(self, template: InlineTemplate) -> str:
        return template.template.format(**template.model_dump())

    def pydantic_form(
        self, model: FormModel[Any], *, token: str | None = None
    ) -> Markup:
        raise NotImplementedError

    def pydantic_form_field(
        self,
        model: type[Any],
        *,
        name: str | None,
        token: str | None,
        removable: bool,
        field: FieldInfo | None,
    ) -> Markup:
        raise NotImplementedError


class FStringTemplateRendererFactory(AbstractTemplateRendererFactory[FString]):
    def __call__(self, request: Request) -> AbstractTemplateRenderer[FString]:
        return FStringTemplateRenderer(request)


@configure
def includeme(conf: Configurator) -> None:
    conf.add_renderer(FStringTemplateRendererFactory())
