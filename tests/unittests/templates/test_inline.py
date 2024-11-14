from typing import Any, Union

import pytest

from fastlife import RedirectResponse
from fastlife.adapters.jinjax.inline import JinjaXTemplate
from fastlife.templates.inline import InlineTemplate, is_inline_template_returned


class MyTemplate(JinjaXTemplate):
    template = ""


def endpoint1() -> InlineTemplate:
    return MyTemplate()


def endpoint2() -> JinjaXTemplate:
    return MyTemplate()


def endpoint3() -> MyTemplate:
    return MyTemplate()


def endpoint4() -> Union[MyTemplate, RedirectResponse]:  # noqa: UP007
    return MyTemplate()


def endpoint5() -> MyTemplate | RedirectResponse:
    return MyTemplate()


def endpoint6() -> RedirectResponse | MyTemplate:
    return MyTemplate()


@pytest.mark.parametrize(
    "endpoint",
    [
        endpoint1,
        endpoint2,
        endpoint3,
        endpoint4,
        endpoint5,
        endpoint6,
    ],
)
def test_is_inline_template_returned(endpoint: Any):
    assert is_inline_template_returned(endpoint) is True


def endpoint7() -> RedirectResponse:
    return RedirectResponse("http://example.net")


def test_is_inline_template_returned_false():
    assert is_inline_template_returned(endpoint7) is False
