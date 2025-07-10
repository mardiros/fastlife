import pytest
from bs4 import PageElement


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Icon name="minus"/>""",
            """
            <svg
                aria-hidden="true"
                fill="currentColor"
                viewbox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path clip-rule="evenodd"
                    d="M4.25 12a.75.75 0 0 1 .75-.75h14a.75.75 0 0 1 0 1.5H5a.75.75 0 0 1-.75-.75Z"
                    fill-rule="evenodd"></path>
            </svg>
            """,
            id="icon",
        ),
        pytest.param(
            """<Icon name="minus" id="hyphen-1"/>""",
            """
            <svg
                id="hyphen-1"
                aria-hidden="true"
                fill="currentColor"
                viewbox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path clip-rule="evenodd"
                    d="M4.25 12a.75.75 0 0 1 .75-.75h14a.75.75 0 0 1 0 1.5H5a.75.75 0 0 1-.75-.75Z"
                    fill-rule="evenodd"></path>
            </svg>
            """,
            id="icon-id",
        ),
        pytest.param(
            """<Icon name="minus" class="p-4"/>""",
            """
            <svg
                class="p-4"
                aria-hidden="true"
                fill="currentColor"
                viewbox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path clip-rule="evenodd"
                    d="M4.25 12a.75.75 0 0 1 .75-.75h14a.75.75 0 0 1 0 1.5H5a.75.75 0 0 1-.75-.75Z"
                    fill-rule="evenodd"></path>
            </svg>
            """,
            id="icon-class",
        ),
        pytest.param(
            """<Icon name="minus" id="hyp" class="danger" title="deletion protocol"/>""",
            """
            <svg
                id="hyp"
                class="danger"
                aria-hidden="true"
                fill="currentColor"
                viewbox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path clip-rule="evenodd"
                    d="M4.25 12a.75.75 0 0 1 .75-.75h14a.75.75 0 0 1 0 1.5H5a.75.75 0 0 1-.75-.75Z"
                    fill-rule="evenodd"><title>deletion protocol</title></path>
            </svg>
            """,
            id="icon-id-class-title",
        ),
    ],
)
def test_Icon(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
