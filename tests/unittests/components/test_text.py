import pytest
from bs4 import PageElement


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<P>paragraph</P>""",
            """<p class="text-base text-neutral-900 dark:text-white">paragraph</p>""",
            id="p",
        ),
        pytest.param(
            """<P class="p">paragraph</P>""",
            """<p class="p">paragraph</p>""",
            id="p-css",
        ),
    ],
)
def test_P(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
