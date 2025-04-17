from collections.abc import Mapping

from playwright.async_api import Page, expect
from tursu import then

from tests.functionals.steps.form import Any


@then('the user sees the text "{text}"')
async def assert_text(page: Page, text: str):
    loc = page.get_by_text(text)
    await expect(loc).to_be_visible()


@then("the user sees the json")
async def assert_json(page: Page, response: Any, doc_string: Mapping[str, Any]):
    actual_json = await (await response.get_response()).json()
    assert actual_json == doc_string


@then('the user sees the python set in "{field}"')
async def assert_json_contains_set(
    page: Page, response: Any, doc_string: set[str], field: str
):
    actual_json = await (await response.get_response()).json()
    assert set(actual_json[field]) == doc_string
