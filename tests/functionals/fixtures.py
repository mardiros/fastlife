from multiprocessing import Process
from typing import Any, Iterator

from behave import fixture  # type: ignore

from tests.fastlife_app.entrypoint import main


@fixture
def fastlife_app(context: Any, **kwargs: Any) -> Iterator[None]:
    proc = Process(target=main, daemon=True)
    proc.start()
    yield
    proc.kill()


@fixture
def browser(context: Any, **kwargs: Any) -> Iterator[None]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        # browser = p.firefox.launch(headless=False, slow_mo=50)
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context.browser = browser.new_page(base_url="http://localhost:8888")
        yield
        browser.close()


if __name__ == "__main__":
    main()
