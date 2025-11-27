"""
Initialize a session.


The session :attr:`fastlife.config.settings.Settings.session_secret_key` must
be set in order to create a session.

This secret is used to sign session content in order to prevent malicious user
to write their own session content. Note that the provided session implementation
does not cipher session content, it just sign. No secret should be placed in the
session.
"""

from fastlife import Configurator, configure

from .middleware import XBackendTag


@configure
def includeme(config: Configurator) -> None:
    settings = config.registry.settings
    if settings.backend_tag_header_value:
        config.add_middleware(
            XBackendTag,
            tag=settings.backend_tag_header_value,
            header_name=settings.backend_tag_header_name,
        )
