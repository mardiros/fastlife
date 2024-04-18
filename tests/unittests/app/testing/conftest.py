import bs4
import pytest

from fastlife.testing.testclient import Element, WebForm, WebTestClient


@pytest.fixture()
def element(html: str, client: WebTestClient):
    tag = bs4.BeautifulSoup(html.strip(), "html.parser")
    return Element(client, tag.contents[0])  # type: ignore


@pytest.fixture
def webform(client: WebTestClient, element: Element) -> WebForm:
    return WebForm(client, "http://localhost.local/", element)
