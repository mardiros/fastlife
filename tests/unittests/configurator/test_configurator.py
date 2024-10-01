import pytest
from fastapi import FastAPI

from fastlife.config.configurator import (
    ConfigurationError,
    Configurator,
    OpenApiTag,
    Settings,
)
from fastlife.testing.testclient import WebTestClient

# from fastlife.config.registry import cleanup_registry


async def test_app():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    app = conf.build_asgi_app()
    assert isinstance(app, FastAPI)


async def test_include():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    conf.include("tests.fastlife_app", ignore=".views.api")
    assert len(conf.build_asgi_app().routes) != 0


def test_add_open_tag():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:components"))
    conf.add_open_tag(OpenApiTag(name="foo", description="Foos foo"))

    with pytest.raises(ConfigurationError) as ctx:
        conf.add_open_tag(OpenApiTag(name="foo", description="Foo's bar"))

    assert str(ctx.value) == "Tag foo can't be registered twice."


def test_add_renderer(settings: Settings):
    conf = Configurator(settings=settings)
    conf.include("tests.fastlife_app.adapters")
    conf.include("tests.fastlife_app.views", ignore=".api")
    app = conf.build_asgi_app()
    client = WebTestClient(app, settings=settings)
    resp = client.get("/f-string")
    assert resp.text == "Hello world!\n"
