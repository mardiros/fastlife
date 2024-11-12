from typing import Any

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


def test_include(conf: Configurator):
    conf.include("tests.fastlife_app", ignore=".views.api")
    assert len(conf.build_asgi_app().routes) != 0


def test_include_relative(conf: Configurator):
    conf.include("...fastlife_app", ignore=".views.api")
    assert len(conf.build_asgi_app().routes) != 0


@pytest.mark.parametrize(
    "module,expected_error",
    [
        pytest.param(
            "_random_module_that_dont_exists",
            "Can't resolve _random_module_that_dont_exists",
            id="unexisting module",
        ),
        pytest.param(
            ".random_module_that_dont_exists",
            "Can't resolve .random_module_that_dont_exists",
            id="unexisting relative module",
        ),
        pytest.param(
            ".my_broken_collection.subtruc",
            "Can't resolve .my_broken_collection.subtruc",
            id="unexisting relative sub module",
        ),
    ],
)
def test_include_raises_configuration_error(
    conf: Configurator, module: str, expected_error: str
):
    with pytest.raises(ConfigurationError) as exc:
        conf.include(module)
    assert str(exc.value) == expected_error


def test_add_openapi_tag(conf: Configurator):
    conf.add_openapi_tag(OpenApiTag(name="foo", description="Foos foo"))

    with pytest.raises(ConfigurationError) as ctx:
        conf.add_openapi_tag(OpenApiTag(name="foo", description="Foo's bar"))

    assert str(ctx.value) == "Tag foo can't be registered twice."


@pytest.mark.parametrize("route", ["/f-string", "/inline-f-string"])
def test_add_renderer(conf: Configurator, settings: MySettings, route: str):
    conf.include("tests.fastlife_app.adapters")
    conf.include("tests.fastlife_app.views", ignore=".api")
    app = conf.build_asgi_app()
    client = WebTestClient(app, settings=settings)
    resp = client.get(route)
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


@pytest.mark.parametrize("params", [{}])
async def test_global_vars(conf: Configurator, dummy_request_param: Any):
    def get_synchronous_hook():
        return "synchronous_hook"

    def get_synchronous_info(request: Any):
        return "synchrounos"

    async def authenticated_user(request: Any):
        return "anonymous"

    conf.add_renderer_global("foo", "bar")
    conf.add_renderer_global("synchronous_hook", get_synchronous_hook, evaluate=False)
    conf.add_renderer_global("sync_nfo", get_synchronous_info)
    conf.add_renderer_global("authenticated_user", authenticated_user)

    rglobals: Any = await conf._build_renderer_globals(  # type: ignore
        dummy_request_param
    )
    lczr = dummy_request_param.registry.localizer(dummy_request_param)
    assert rglobals == {
        "foo": "bar",
        "synchronous_hook": get_synchronous_hook,
        "sync_nfo": "synchrounos",
        "authenticated_user": "anonymous",
        "csrf_token": {
            "name": "csrf_token",
            "value": "",
        },
        "dgettext": lczr.dgettext,
        "dngettext": lczr.dngettext,
        "dnpgettext": lczr.dnpgettext,
        "dpgettext": lczr.dpgettext,
        "gettext": lczr.gettext,
        "ngettext": lczr.ngettext,
        "npgettext": lczr.npgettext,
        "pgettext": lczr.pgettext,
        "request": dummy_request_param,
    }
