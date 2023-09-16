from fastapi import FastAPI

import tests.fastlite_app.views
from fastlife.configurator.configurator import Configurator


async def test_app():
    conf = Configurator()
    app = conf.get_app()
    assert isinstance(app, FastAPI)


async def test_include():
    conf = Configurator()
    conf.include(tests.fastlite_app.views)
    assert len(conf.get_app().routes) != 0
