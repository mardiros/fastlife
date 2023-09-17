from fastapi import FastAPI

from fastlife.configurator.configurator import Configurator, Settings
from fastlife.configurator.registry import cleanup_registry


async def test_app():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:templates"))
    app = conf.get_app()
    assert isinstance(app, FastAPI)
    cleanup_registry()


async def test_include():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:templates"))
    conf.include("tests.fastlife_app")
    assert len(conf.get_app().routes) != 0
    cleanup_registry()
