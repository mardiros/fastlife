import pytest
from multidict import MultiDict

from fastlife.testing.testclient import WebForm


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param(
            """
            <form>
                <input type="hidden" name="csrf" value="token">
                <button name="shoes" value="0">Choose<button>
            </form>
            """,
            {  # type: ignore
                "csrf": "token",
                "shoes": "0",
                "origin": "http://localhost.local/",
            },
            id="origin",
        ),
        pytest.param(
            """
            <form post="/html" method="post">
                <input type="hidden" name="csrf" value="token">
                <button name="shoes" value="0">Choose<button>
            </form>
            """,
            {  # type: ignore
                "csrf": "token",
                "shoes": "0",
                "origin": "/html",
            },
            id="origin",
        ),
        pytest.param(
            """
            <form hx-post="/htmx">
                <input type="hidden" name="csrf" value="token">
                <button name="shoes" value="0">Choose<button>
            </form>
            """,
            {  # type: ignore
                "csrf": "token",
                "shoes": "0",
                "origin": "/htmx",
            },
            id="origin",
        ),
        pytest.param(
            """
            <form hx-post="/htmx">
                <input type="checkbox" name="colors" value="red">
                <input type="checkbox" name="colors" value="green" checked>
                <input type="checkbox" name="colors" value="blue" checked>
                <input type="hidden" name="csrf" value="token">
                <button name="shoes" value="0">Choose<button>
            </form>
            """,
            MultiDict(  # type: ignore
                [
                    ("colors", "green"),
                    ("colors", "blue"),
                    ("csrf", "token"),
                    ("shoes", "0"),
                    ("origin", "/htmx"),
                ]
            ),
            id="checkboxes",
        ),
    ],
)
def test_submit(webform: WebForm, expected: str):
    resp = webform.button("Choose").submit()
    assert resp.form._formdata == expected  # type: ignore
