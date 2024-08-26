from fastapi import FastAPI

from fastlife.config.configurator import Configurator, Settings

# from fastlife.config.registry import cleanup_registry


async def test_app():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:templates"))
    app = conf.get_asgi_app()
    assert isinstance(app, FastAPI)


async def test_include():
    conf = Configurator(Settings(template_search_path="tests.fastlife_app:templates"))
    conf.include("tests.fastlife_app")
    assert len(conf.get_asgi_app().routes) != 0
