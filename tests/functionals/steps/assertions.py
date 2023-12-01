# type: ignore

from typing import Any

from behave import then

"""
Debug in the devtools of firefox

function getElementByXpath(path) {
  return document.evaluate(
    path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
  ).singleNodeValue;
}
"""


@then('I see the text "{text}"')
def assert_text(context: Any, text: str):
    text = text.replace("'", "\\'")
    context.browser.find_element_by_xpath(
        f"//*[contains(text(), '{text}') or .='{text}']"
    )


@then('I don\'t see the text "{text}"')
def assert_not_text(context: Any, text: str):
    text = text.replace("'", "\\'")
    context.browser.dont_find_element_by_xpath(
        f"//*[contains(text(), '{text}') or .='{text}']"
    )


@then('I see the heading "{text}"')
def assert_h1(context: Any, text: str):
    context.browser.find_element_by_xpath(f"//h1[contains(text(), '{text}')]")
