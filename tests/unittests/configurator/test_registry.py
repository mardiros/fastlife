from fastlife.configurator import registry
from fastlife.configurator.settings import Settings


def test_initialize_registry(settings: Settings):
    reg = registry.initialize_registry(settings)
    assert reg.settings == settings
    assert reg.__class__.__name__ == "AppRegistry"
