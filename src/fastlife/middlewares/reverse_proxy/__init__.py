from fastlife import Configurator, configure

from .x_forwarded import XForwardedStar


@configure
def includeme(config: Configurator) -> None:
    settings = config.registry.settings
    if settings.decode_reverse_proxy_headers:
        config.add_middleware(XForwardedStar)
