# type: ignore
import ast
import json

from behave import then
from playwright.sync_api import expect

from tests.functionals.context import Context


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


@then("I see the json")
def assert_json(context: Context):
    assert context.response is not None
    actual_json = context.response.json()
    expected = json.loads(context.text)
    assert actual_json == expected, f"{context.text} != {json.dumps(actual_json)}"


@then('I see the python set "{value}" in "{field}"')
def assert_json_contains_set(context: Context, value: str, field: str):
    assert context.response is not None
    actual_json = context.response.json()
    expected = ast.literal_eval(value)
    assert set(actual_json[field]) == expected, (
        f'{{"{field}": {expected} }} != {{"{field}": {set(actual_json[field])}}}'
    )
