"""A dummy view to test the add_renderer"""

from typing import Annotated, Any, Mapping

from fastapi import Path

from fastlife import Request, view_config
from fastlife.config.configurator import Configurator, configure


@view_config(
    "hello-i18n", "/{locale}/hello", template="i18n.Hello.jinja", methods=["GET"]
)
async def hello_i18n(locale: Annotated[str, Path(...)]) -> Mapping[str, Any]:
    return {}


def locale_negociator(request: Request) -> str:
    return request.path_params.get("locale") or request.registry.settings.default_locale


@configure
def includeme(config: Configurator):
    config.set_locale_negociator(locale_negociator)
