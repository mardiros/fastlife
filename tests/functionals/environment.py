from collections import defaultdict
from typing import Any

from behave import use_fixture  # type: ignore
from fixtures import browser, fastlife_app  # type: ignore


def before_scenario(context: Any, scenario: Any):
    context.stash = defaultdict(dict)
    use_fixture(fastlife_app, context)
    use_fixture(browser, context)
