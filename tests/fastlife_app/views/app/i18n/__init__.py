from fastlife import Request
from fastlife.config.configurator import Configurator, configure


def locale_negociator(request: Request) -> str:
    return request.path_params.get("locale") or request.registry.settings.default_locale


@configure
def includeme(config: Configurator):
    config.set_locale_negociator(locale_negociator)
    config.add_translation_dirs("tests.fastlife_app:locales")
