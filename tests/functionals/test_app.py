from playwright.sync_api import Page, expect


def test_has_title(client: Page):
    client.goto("http://localhost:8888/")

    locator = client.locator("h1")
    expect(locator).to_have_text("Hello World!")


def test_union_type_replace_button_by_form(client: Page):
    client.goto("http://localhost:8888/autoform")

    client.get_by_role("button", name="Dog").click()
    client.get_by_label("nick").fill("marvin")
    client.get_by_label("breed").select_option("Labrador")
