import pytest

from fastlife.config.configurator import ConfigurationError, Configurator
from fastlife.settings import Settings


def test_resource_missing_path():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    with pytest.raises(ConfigurationError) as ctx:
        conf.include("tests.unittests.config.my_broken_resource")

    assert str(ctx.value) == "path not set on resource foo"


def test_collection_missing_collection_path():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    with pytest.raises(ConfigurationError) as ctx:
        conf.include("tests.unittests.config.my_broken_collection")

    assert str(ctx.value) == "collection_path not set on resource foo"
