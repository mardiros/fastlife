from fastlife import configure, Configurator
from fastlife.security.policy import InsecurePolicy


@configure
def includeme(conf: Configurator):
    conf.set_security_policy(InsecurePolicy)
