from playwright.sync_api import Page, expect


def test_has_title(client: Page):
    client.goto("http://localhost:8888/")

    locator = client.locator("h1")
    expect(locator).to_have_text("Hello World!")
