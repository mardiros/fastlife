import pytest
from bs4 import PageElement

a_css = (
    "text-primary-600 hover:text-primary-500 hover:underline "
    "dark:text-primary-300 dark:hover:text-primary-400"
)


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<A href="/">text</A>""",
            f"""
            <a hx-target="#maincontent"
               class="{a_css}"
               href="/"
               hx-get="/"
               hx-push-url="true"
               hx-swap="innerHTML show:body:top"
               >text</a>
            """,
            id="default",
        ),
        pytest.param(
            """
            <A href='/js-disabled'
               hx-get="/load-it"
               hx-push-url="/load-that"
               hx-swap='innerHTML'
               class='mine'>text</A>
            """,
            """
            <a href='/js-disabled'
               hx-get="/load-it"
               hx-target="#maincontent"
               class="mine"
               hx-push-url="/load-that"
               hx-swap="innerHTML"
               >text</a>
            """,
            id="hx-push-url",
        ),
        pytest.param(
            """
            <A href='/js-disabled'
               hx-get="/load-it"
               hx-swap='innerHTML'
               class='mine'>text</A>
            """,
            """
            <a href='/js-disabled'
               hx-get="/load-it"
               hx-target="#maincontent"
               class="mine"
               hx-push-url="true"
               hx-swap="innerHTML"
               >text</a>
            """,
            id="hx-link",
        ),
        pytest.param(
            """<A href='/' hx-disable>text</A>""",
            f"""
            <a href="/"
               class="{a_css}"
               href="/"
               hx-disable=""
               hx-get="/"
               hx-swap="innerHTML show:body:top"
               hx-target="#maincontent"
               hx-push-url="true"
               >text</a>
            """,
            id="hx-disable",
        ),
        pytest.param(
            """<A href='/' hx-disabled-elt='this'>text</A>""",
            f"""
            <a href="/"
               class="{a_css}"
               hx-disabled-elt="this"
               hx-get="/"
               hx-swap="innerHTML show:body:top"
               hx-target="#maincontent"
               hx-push-url="true"
               >text</a>""",
            id="hx-disable-elt",
        ),
    ],
)
def test_A(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
