from fastlife import Configurator, configure
from fastlife.shared_utils.resolver import resolve

from .middleware import SessionMiddleware


@configure
def includeme(config: Configurator) -> None:
    settings = config.registry.settings
    session_serializer = resolve(settings.session_serializer)
    if settings.session_secret_key:
        config.add_middleware(
            SessionMiddleware,
            cookie_name=settings.session_cookie_name,
            secret_key=settings.session_secret_key,
            duration=settings.session_duration,
            cookie_path=settings.session_cookie_path,
            cookie_same_site=settings.session_cookie_same_site,
            cookie_secure=settings.session_cookie_secure,
            cookie_domain=settings.session_cookie_domain,
            serializer=session_serializer,
        )
