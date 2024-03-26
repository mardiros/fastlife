import pytest

from fastlife.configurator import registry
from fastlife.configurator.settings import Settings


def test_initialize_registry(settings: Settings):
    assert registry.DEFAULT_REGISTRY is None
    registry.initialize_registry(settings)
    assert registry.DEFAULT_REGISTRY is not None
    # assert isinstance(registry.DEFAULT_REGISTRY, registry.AppRegistry)
    assert registry.DEFAULT_REGISTRY.settings == settings

    with pytest.raises(ValueError):
        registry.initialize_registry(settings)

    registry.cleanup_registry()
    assert registry.DEFAULT_REGISTRY is None
