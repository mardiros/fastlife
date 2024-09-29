from fastlife import Configurator, configure
from fastlife.security.policy import InsecurePolicy


@configure
def includeme(conf: Configurator):
    conf.set_security_policy(InsecurePolicy)
