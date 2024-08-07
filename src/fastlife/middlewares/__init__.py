from fastlife import Configurator, configure


@configure
def includeme(config: Configurator) -> None:
    config.include(".reverse_proxy")
    config.include(".session")
