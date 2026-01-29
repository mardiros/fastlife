import pytest
from bs4 import PageElement

details_css = "border border-neutral-100 mt-4 p-4 rounded-m"

summary_css = "flex items-center items-center font-medium cursor-pointer"

h3_css = (
    "block font-bold font-sans leading-tight text-3xl text-neutral-900 "
    "tracking-tight dark:text-white md:text-3xl"
)

chevron = """<svg aria-hidden="true"
    class="w-8 h-8 transform transition-transform duration-300 rotate-90"
    fill="currentColor"
    id="my-summary-icon"
    viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path clip-rule="evenodd"
        d="M16.28 11.47a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06-1.06L14.69 12 7.72 5.03a.75.75 0 0 1 1.06-1.06l7.5 7.5Z"
        fill-rule="evenodd"></path></svg>"""


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """
            <Details>
              <Summary id="my-summary">
                <H3 class={globals.H3_SUMMARY_CLASS}>A title</H3>
              </Summary>
              <div>Some content</div>
            </Details>
            """,
            f"""
            <details class="{details_css}" open="">
                <summary
                    class="{summary_css}"
                    id="my-summary"
                    onclick="document.getElementById('my-summary-icon').classList.toggle('rotate-90')"
                    style="list-style: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;">
                    {chevron}
                    <h3 class="{h3_css}">A title</h3>
                </summary>
                <div>Some content</div>
            </details>
            """,
            id="default",
        ),
    ],
)
def test_Summary(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
