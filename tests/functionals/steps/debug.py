import asyncio
from typing import Any

from tursu import given, then, when


@given("I wait")
@when("I wait")
@then("I wait")
async def i_wait(context: Any) -> None:
    await asyncio.sleep(60 * 5)
