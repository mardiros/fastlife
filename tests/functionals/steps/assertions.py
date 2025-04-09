from collections.abc import Mapping

from playwright.sync_api import Page, expect
from tursu import then

from tests.functionals.steps.form import Any


@then('the user see the text "{text}"')
def assert_text(page: Page, text: str):
    loc = page.get_by_text(text)
    expect(loc).to_be_visible()


@then('I don\'t see the text "{text}"')
def assert_not_text(page: Page, text: str):
    loc = page.get_by_text(text)
    expect(loc).not_to_be_visible()


@then('I see the heading "{text}"')
def assert_h1(page: Page, text: str):
    loc = page.locator(f"xpath=//h1[contains(text(), '{text}')]")
    expect(loc).to_be_visible()


@then("the user see the json")
def assert_json(page: Page, response: Any, doc_string: Mapping[str, Any]):
    actual_json = response.get_response().json()
    assert actual_json == doc_string


@then('the user see the python set in "{field}"')
def assert_json_contains_set(
    page: Page, response: Any, doc_string: set[str], field: str
):
    actual_json = response.get_response().json()
    assert set(actual_json[field]) == doc_string
