import multiprocessing

import pytest
from playwright.sync_api import Browser, Page

from tests.fastlife_app.entrypoint import serve_app


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
