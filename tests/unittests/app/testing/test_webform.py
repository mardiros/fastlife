from typing import Any

import pytest
from multidict import MultiDict

from fastlife.testing.testclient import WebForm


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="text" name="firstname" value="alice">
                <input type="text" name="lastname">
                <select name="color">
                    <option value="blue">blue</option>
                    <option value="red" selected>red</option>
                </select>
                <select name="size">
                    <option value="s">s</option>
                    <option value="m">m</option>
                </select>
                <select name="tempo">
                    <option>piano</option>
                    <option>allegro</option>
                </select>
                <input type="hidden" name="csrf" value="token">
            </form>
            """,
            id="form",
        )
    ],
)
def test_default_value(webform: WebForm):
    assert webform._formdata == {  # type: ignore
        "csrf": "token",
        "firstname": "alice",
        "lastname": "",
        "color": "red",
        "size": "s",
        "tempo": "piano",
    }


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="text" name="firstname">
                <input type="text" name="lastname">
                <input type="checkbox" name="colors" value="red">
                <input type="checkbox" name="colors" value="green" checked>
                <input type="checkbox" name="colors" value="blue" checked>
                <input type="hidden" name="csrf" value="token">
            </form>
        """,
            id="text",
        )
    ],
)
def test_set_input_value(webform: WebForm):
    webform.set("firstname", "bob")
    webform.set("lastname", "marley")
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("firstname", "bob"),
            ("lastname", "marley"),
            ("colors", "green"),
            ("colors", "blue"),
            ("csrf", "token"),
        ]
    )


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param(
            """<form><select name="name"></select></form>""",
            '"name" is a <select>, use select() instead',
            id="select",
        ),
        pytest.param(
            """<form></form>""",
            '"name" does not exists',
            id="unkown",
        ),
    ],
)
def test_set_exception(webform: WebForm, expected: str):
    with pytest.raises(ValueError) as cxt:
        webform.set("name", "medium")
    assert str(cxt.value) == expected


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <select name="size">
                    <option value="s">small</option>
                    <option value="m">medium</option>
                </select>
                <select name="tempo">
                    <option>piano</option>
                    <option>allegro</option>
                </select>
                <select name="foobar">
                    <option>foo</option>
                    <option>bar</option>
                </select>
                <input type="hidden" name="csrf" value="token">
            </form>
            """,
            id="select",
        )
    ],
)
def test_select_value(webform: WebForm):
    webform.select("size", "medium")
    webform.select("tempo", "allegro")
    assert webform._formdata == {  # type: ignore
        "csrf": "token",
        "size": "m",
        "tempo": "allegro",
        "foobar": "foo",
    }


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param(
            """<form><input type="text" name="name" value=""></form>""",
            "name is a <input>, use set() instead",
            id="input",
        ),
        pytest.param(
            """<form></form>""",
            '"name" does not exists',
            id="unkown",
        ),
        pytest.param(
            """
            <form>
                <select name="name" class="css">
                    <option>piano</option>
                    <option>allegro</option>
                </select>
            </form>
            """,
            'No option subito in <select name="name">',
            id="select",
        ),
    ],
)
def test_select_exception(webform: WebForm, expected: str):
    with pytest.raises(ValueError) as cxt:
        webform.select("name", "subito")
    assert str(cxt.value) == expected


@pytest.mark.parametrize(
    "html,call_args,expected",
    [
        pytest.param(
            """
            <form>
                <button name="shoes" value="0">Choose</button>
            </form>
            """,
            ("Choose",),
            {"shoes": "0"},
            id="first",
        ),
        pytest.param(
            """
            <form>
                <button name="shoes" value="a">Choose</button>
                <button name="shoes" value="b">Choose</button>
                <button name="shoes" value="c">Choose</button>
            </form>
            """,
            ("Choose", 1),
            {"shoes": "b"},
            id="pos",
        ),
    ],
)
def test_button_value(webform: WebForm, call_args: Any, expected: str):
    assert webform._formdata == {}  # type: ignore

    webform.button(*call_args)
    assert webform._formdata == expected  # type: ignore


@pytest.mark.parametrize(
    "html,call_args,expected",
    [
        pytest.param(
            """
            <form>
                <button name="shoes" value="0">Choose</button>
            </form>
            """,
            ("Shoes",),
            'Button "Shoes" not found',
            id="first",
        ),
        pytest.param(
            """
            <form>
                <button name="shoes" value="a">Choose</button>
                <button name="shoes" value="b">Choose</button>
                <button name="shoes" value="c">Choose</button>
            </form>
            """,
            ("Choose", 4),
            'Button "Choose" not found at position 4',
            id="pos",
        ),
    ],
)
def test_button_error(webform: WebForm, call_args: Any, expected: str):
    with pytest.raises(ValueError) as ctx:
        webform.button(*call_args)
    assert str(ctx.value) == expected


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="hidden" name="csrf" value="token">
                <button name="shoes" value="0">Choose<button>
            </form>
            """,
            id="form",
        ),
    ],
)
def test_in(webform: WebForm):
    assert "csrf" in webform
    assert "shoes" not in webform
