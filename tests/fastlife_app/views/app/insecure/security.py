from fastlife import Configurator, configure
from fastlife.service.security_policy import InsecurePolicy


@configure
def includeme(conf: Configurator) -> None:
    conf.set_security_policy(InsecurePolicy)
