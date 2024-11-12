from typing import Any, Union

import pytest

from fastlife.templates.inline import InlineTemplate, is_inline_template_returned
from tests.fastlife_app.views.app.admin.login import JinjaXTemplate, RedirectResponse


class Mytemplate(JinjaXTemplate):
    template = ""


def endpoint1() -> InlineTemplate: ...


def endpoint2() -> JinjaXTemplate: ...


def endpoint3() -> Mytemplate: ...


def endpoint4() -> Union[Mytemplate, RedirectResponse]: ...  # noqa: UP007


def endpoint5() -> Mytemplate | RedirectResponse: ...


def endpoint6() -> RedirectResponse | Mytemplate: ...


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


def endpoint7() -> RedirectResponse: ...


def test_is_inline_template_returned_false():
    assert is_inline_template_returned(endpoint7) is False
