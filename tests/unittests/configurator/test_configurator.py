from fastapi import FastAPI
from fastlife.configurator.configurator import Configurator


async def test_app():
    conf = Configurator()
    app = conf.get_app()
    assert isinstance(app, FastAPI)
