from fastlife import Configurator
from fastlife.shared_utils import resolver


def test_resolve():
    ConfiguratorClass = resolver.resolve("fastlife:Configurator")
    assert ConfiguratorClass is Configurator
