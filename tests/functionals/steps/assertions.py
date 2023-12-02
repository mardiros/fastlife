# type: ignore

from behave import then
from playwright.sync_api import Page, expect


class Context:
    browser: Page


@then('I see the text "{text}"')
def assert_text(context: Context, text: str):
    loc = context.browser.get_by_text(text)
    expect(loc).to_be_visible()


@then('I don\'t see the text "{text}"')
def assert_not_text(context: Context, text: str):
    loc = context.browser.get_by_text(text)
    expect(loc).not_to_be_visible()


@then('I see the heading "{text}"')
def assert_h1(context: Context, text: str):
    loc = context.browser.locator(f"xpath=//h1[contains(text(), '{text}')]")
    expect(loc).to_be_visible()
