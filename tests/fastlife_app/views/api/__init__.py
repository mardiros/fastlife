"""APIs routes"""

from fastlife import Configurator, configure

from .security import OAuth2SecurityPolicy


@configure
def includeme(config: Configurator):
    config.set_api_security_policy(OAuth2SecurityPolicy)
