# type: ignore
import time
from typing import Any

from behave import given, then, when


@given("I wait")
@when("I wait")
@then("I wait")
def i_wait(context: Any) -> None:
    time.sleep(60 * 5)
