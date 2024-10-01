"""
A middleware that update the request scope for https behind a proxy.

The attempt of this middleware is to fix Starlette behavior that use client and scheme
header based on the header ``x-forwarded-*`` headers and the ``x-real-ip``.

the ``x-forwarded-for`` header is not parsed to find the appropriate value,
the ``x-real-ip`` is used.
notethat the ``x-forwarded-port`` header is not used.

Note that uvicorn or hypercorn offer the same kind middleware.

Norw, every website is in https, so, this middleware is active by default.
"""

from fastlife import Configurator, configure

from .x_forwarded import XForwardedStar

__all__ = ["XForwardedStar"]


@configure
def includeme(config: Configurator) -> None:
    settings = config.registry.settings
    if settings.decode_reverse_proxy_headers:
        config.add_middleware(XForwardedStar)
