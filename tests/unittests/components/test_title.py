import pytest
from bs4 import PageElement


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H1>title</H1>""",
            """<h1 class="block font-bold font-sans leading-tight pb-4 text-5xl
            text-neutral-900 tracking-tight dark:text-white md:text-4xl">title</h1>""",
            id="H1",
        ),
        pytest.param(
            """<H1 class="h1">title</H1>""",
            """<h1 class="h1">title</h1>""",
            id="H1-css",
        ),
    ],
)
def test_render_H1(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H2>title</H2>""",
            """<h2 class="block font-bold font-sans leading-tight pb-4 text-4xl
            text-neutral-900 tracking-tight dark:text-white md:text-4xl">title</h2>""",
            id="H2",
        ),
        pytest.param(
            """<H2 class="h2">title</H2>""",
            """<h2 class="h2">title</h2>""",
            id="H2-css",
        ),
    ],
)
def test_render_H2(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H3>title</H3>""",
            """<h3 class="block font-bold font-sans leading-tight pb-4 text-3xl
            text-neutral-900 tracking-tight dark:text-white md:text-3xl">title</h3>""",
            id="H3",
        ),
        pytest.param(
            """<H3 class="h3">title</H3>""",
            """<h3 class="h3">title</h3>""",
            id="H3-css",
        ),
    ],
)
def test_render_H3(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H4>title</H4>""",
            """<h4 class="block font-bold font-sans leading-tight pb-4 text-2xl
            text-neutral-900 tracking-tight dark:text-white md:text-2xl">title</h4>""",
            id="H4",
        ),
        pytest.param(
            """<H4 class="h4">title</H4>""",
            """<h4 class="h4">title</h4>""",
            id="H4-css",
        ),
    ],
)
def test_render_H4(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H5>title</H5>""",
            """<h5 class="block font-bold font-sans leading-tight pb-4 text-xl
            text-neutral-900 tracking-tight dark:text-white md:text-xl">title</h5>""",
            id="H5",
        ),
        pytest.param(
            """<H5 class="h5">title</H5>""",
            """<h5 class="h5">title</h5>""",
            id="H5-css",
        ),
    ],
)
def test_render_H5(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<H6>title</H6>""",
            """<h6 class="block font-bold font-sans leading-tight pb-4 text-l
            text-neutral-900 tracking-tight dark:text-white md:text-l">title</h6>""",
            id="H6",
        ),
        pytest.param(
            """<H6 class="h6">title</H6>""",
            """<h6 class="h6">title</h6>""",
            id="H6-css",
        ),
    ],
)
def test_render_H6(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
