import pytest
from fastapi import FastAPI

from fastlife.config.configurator import (
    ConfigurationError,
    Configurator,
    OpenApiTag,
    Settings,
)

# from fastlife.config.registry import cleanup_registry


async def test_app():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    app = conf.build_asgi_app()
    assert isinstance(app, FastAPI)


async def test_include():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    conf.include("tests.fastlife_app")
    assert len(conf.build_asgi_app().routes) != 0


def test_add_open_tag():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    conf.add_open_tag(OpenApiTag(name="foo", description="Foos foo"))

    with pytest.raises(ConfigurationError) as ctx:
        conf.add_open_tag(OpenApiTag(name="foo", description="Foo's bar"))

    assert str(ctx.value) == "Tag foo can't be registered twice."
