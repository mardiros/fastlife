# type: ignore

from behave import given, when
from playwright.sync_api import Page


class Context:
    browser: Page


@given('anonymous user on "{path}"')
@when('I visit "{path}"')
def i_visit(context: Context, path: str):
    context.browser.goto(path)
