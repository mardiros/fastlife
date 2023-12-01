# type: ignore
from typing import Any

from behave import given, when


@given('anonymous user on "{path}"')
@when('I visit "{path}"')
def i_visit(context: Any, path: str):
    context.browser.get(path)
