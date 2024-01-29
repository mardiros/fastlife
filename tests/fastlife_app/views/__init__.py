from fastlife import Configurator, configure


@configure
def includeme(config: Configurator):
    config.include(".home")
    config.include(".login")
    config.include(".secured")
