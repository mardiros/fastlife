import pytest
from fastapi import FastAPI

from fastlife.config.configurator import (
    ConfigurationError,
    Configurator,
    OpenApiTag,
    Settings,
)
from fastlife.testing.testclient import WebTestClient
from tests.fastlife_app.config import MySettings

# from fastlife.config.registry import cleanup_registry


@pytest.fixture
def conf(settings: Settings) -> Configurator:
    return Configurator(settings)


async def test_app(conf: Configurator):
    app = conf.build_asgi_app()
    assert isinstance(app, FastAPI)


async def test_include(conf: Configurator):
    conf.include("tests.fastlife_app", ignore=".views.api")
    assert len(conf.build_asgi_app().routes) != 0


def test_add_open_tag(conf: Configurator):
    conf.add_open_tag(OpenApiTag(name="foo", description="Foos foo"))

    with pytest.raises(ConfigurationError) as ctx:
        conf.add_open_tag(OpenApiTag(name="foo", description="Foo's bar"))

    assert str(ctx.value) == "Tag foo can't be registered twice."


def test_add_renderer(conf: Configurator, settings: MySettings):
    conf.include("tests.fastlife_app.adapters")
    conf.include("tests.fastlife_app.views", ignore=".api")
    app = conf.build_asgi_app()
    client = WebTestClient(app, settings=settings)
    resp = client.get("/f-string")
    assert resp.text == "Hello world!\n"


def test_all_registered_permissions(conf: Configurator):
    assert conf.all_registered_permissions == []
    conf.include("tests.fastlife_app.views.api")
    assert conf.all_registered_permissions == ["foos:delete", "foos:read", "foos:write"]
    conf.include("tests.fastlife_app.views", ignore=".api")
    assert conf.all_registered_permissions == [
        "admin",
        "foos:delete",
        "foos:read",
        "foos:write",
    ]
