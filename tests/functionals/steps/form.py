# type:ignore

from typing import Any

from behave import when


@when('I fill the field "{aria_label}" with "{value}"')
def fill_input(context: Any, aria_label: str, value: str):
    field = context.browser.find_element_by_xpath(
        f"//input[@aria-label='{aria_label}']"
    )
    field.clear()
    field.send_keys(value)


@when('I click on the button "{aria_label}"')
def fill_input(context: Any, aria_label: str):
    btn = context.browser.find_element_by_xpath(
        f"//button[@aria-label='{aria_label}']"
    )
    btn.click()

