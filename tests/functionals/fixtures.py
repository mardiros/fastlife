import time
from multiprocessing import Process
from typing import Any, Callable, Iterator, List

from behave import fixture  # type: ignore
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.remote.webelement import WebElement

from tests.fastlife_app.entrypoint import serve_app


class Browser:
    def __init__(self, web_root: str) -> None:
        self.browser = Firefox()
        self.web_root = web_root

    def wait_for(
        self,
        method: Callable[..., Any],
        *args: Any,
        timeout: int = 10,
        interval: float = 0.2,
    ):
        start_time = time.time()
        while True:
            try:
                return method(*args)
            except (AssertionError, WebDriverException) as exc:
                if time.time() - start_time > timeout:
                    raise exc
                time.sleep(interval)

    def find_element_by_xpath(self, path: str) -> WebElement:
        return self.wait_for(
            self.browser.find_element,  # type: ignore
            By.XPATH,
            path,
        )

    def dont_find_element_by_xpath(self, path: str) -> None:
        try:
            self.browser.find_element(By.XPATH, path)
        except NoSuchElementException:
            return
        else:
            raise ValueError(f"Element {path} exists")

    def find_elements_by_xpath(self, path: str) -> List[WebElement]:
        return self.wait_for(
            self.browser.find_elements,  # type: ignore
            By.XPATH,
            path,
        )

    def get(self, path: str):
        if path.startswith("/"):
            self.browser.get(f"{self.web_root}{path}")
        else:
            self.browser.get(f"{path}")

    def quit(self):
        self.browser.quit()


@fixture
def fastlife_app(context: Any, **kwargs: Any) -> Iterator[None]:
    proc = Process(target=serve_app, daemon=True)
    proc.start()
    yield
    proc.kill()


@fixture
def browser(context: Any, **kwargs: Any) -> Iterator[None]:
    context.browser = Browser("http://localhost:8888")
    yield
    context.browser.quit()


if __name__ == "__main__":
    serve_app()
