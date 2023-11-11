import asyncio
import multiprocessing

import pytest
from hypercorn.asyncio import serve
from hypercorn.config import Config
from playwright.sync_api import Browser, Page

from fastlife import Configurator
from fastlife.configurator.configurator import Settings


async def app():
    conf = Configurator(
        Settings(template_search_path="fastlife:templates,tests.fastlife_app:templates")
    )
    conf.include("tests.fastlife_app.views")
    app = conf.get_app()
    config = Config()
    config.bind = ["0.0.0.0:8888"]
    await serve(app, config)  # type: ignore


def serve_app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app())


@pytest.fixture()
def app_launcher():
    subprocess = multiprocessing.Process(target=serve_app)
    subprocess.start()
    yield
    subprocess.terminate()


@pytest.fixture()
def client(app_launcher, browser: Browser) -> Page:
    page = browser.new_page()
    page.goto("http://localhost:8888/")
    return page
