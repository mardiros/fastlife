# type:ignore

from behave import when
from playwright.sync_api import Page


class Context:
    browser: Page


@when('I fill the field "{label}" with "{value}"')
def fill_input(context: Context, label: str, value: str):
    field = context.browser.get_by_label(label)
    field.clear()
    field.fill(value)


@when('I click on the button "{aria_label}"')
def click_button(context: Context, aria_label: str):
    btn = context.browser.locator(f"xpath=//button[@aria-label='{aria_label}']")
    btn.click()
