import bs4
import pytest
from fastlife.testing.testclient import Element, WebTestClient


@pytest.fixture()
def element(html: str, client: WebTestClient):
    tag = bs4.BeautifulSoup(html, "html.parser")
    return Element(client, tag.contents[0])  # type: ignore
