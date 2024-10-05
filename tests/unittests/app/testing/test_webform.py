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
                <select name="lang" multiple>
                    <option>python</option>
                    <option>javascript</option>
                    <option>ruby</option>
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
                <input type="checkbox" name="colors" value="blue">
                <input type="hidden" name="csrf" value="token">
            </form>
            """,
            id="input",
        )
    ],
)
def test_set_input_value(webform: WebForm):
    webform.set("firstname", "bob")
    webform.set("lastname", "marley")
    webform.set("colors", "blue")
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("firstname", "bob"),
            ("lastname", "marley"),
            ("colors", "green"),
            ("csrf", "token"),
            ("colors", "blue"),
        ]
    )


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="hidden" name="csrf" value="token">
            </form>
            """,
            id="input",
        )
    ],
)
def test_repr(webform: WebForm):
    assert repr(webform) == "<MultiDict('csrf': 'token')>"


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="radio" name="colors" value="red">
                <input type="radio" name="colors" value="green" checked>
                <input type="radio" name="colors" value="blue">
            </form>
            """,
            id="radio",
        )
    ],
)
def test_set_radio(webform: WebForm):
    webform.set("colors", "red")
    webform.set("colors", "blue")
    assert webform._formdata == MultiDict([("colors", "blue")])  # type: ignore


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="radio" name="colors" value="red">
                <input type="radio" name="colors" value="green" checked>
            </form>
            """,
            id="radio",
        )
    ],
)
def test_set_radio_raise(webform: WebForm):
    with pytest.raises(ValueError) as ctx:
        webform.set("colors", "blue")
    assert str(ctx.value) == 'radio "colors" does not contains blue option'


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <input type="checkbox" name="colors" value="red" checked>
                <input type="checkbox" name="colors" value="green" checked>
                <input type="checkbox" name="colors" value="blue">
            </form>
            """,
            id="checkbox",
        )
    ],
)
def test_unset_input_value(webform: WebForm):
    webform.unset("colors", "green")
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("colors", "red"),
        ]
    )


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param(
            """
            <form></form>
            """,
            '"colors" does not exists',
            id="does not exist",
        ),
        pytest.param(
            """
            <form>
                <input type="checkbox" name="colors" value="green" checked>
                <input type="checkbox" name="colors" value="blue">
            </form>
            """,
            '"red" not in "colors"',
            id="missing",
        ),
        pytest.param(
            """
            <form>
                <input type="text" name="colors" value="red" />
            </form>
            """,
            '"colors" is not a checkbox',
            id="text",
        ),
        pytest.param(
            """
            <form>
                <select name="colors">
                    <option>red</option>
                    <option>green</option>
                    <option>blue</option>
                </select>
            </form>
            """,
            '"colors" is not a checkbox',
            id="select",
        ),
    ],
)
def test_unset_raise(webform: WebForm, expected: str):
    with pytest.raises(ValueError) as ctx:
        webform.unset("colors", "red")
    assert str(ctx.value) == expected


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
    "html",
    [
        pytest.param(
            """
            <form>
                <select name="tempo" multiple>
                    <option>piano</option>
                    <option>allegro</option>
                    <option>moderato</option>
                </select>
            </form>
            """,
            id="select",
        )
    ],
)
def test_select_multiple_value(webform: WebForm):
    webform.select("tempo", "allegro")
    webform.select("tempo", "moderato")
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("tempo", "allegro"),
            ("tempo", "moderato"),
        ]
    )


@pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            """
            <form>
                <select name="tempo" multiple>
                    <option>piano</option>
                    <option selected>allegro</option>
                    <option selected>moderato</option>
                </select>
            </form>
            """,
            id="select",
        )
    ],
)
def test_select_multiple_default_value(webform: WebForm):
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("tempo", "allegro"),
            ("tempo", "moderato"),
        ]
    )


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
    "html",
    [
        pytest.param(
            """
            <form>
                <select name="tempo" multiple>
                    <option>piano</option>
                    <option selected>allegro</option>
                    <option selected>moderato</option>
                </select>
            </form>
            """,
            id="select",
        )
    ],
)
def test_unselect_multiple_value(webform: WebForm):
    webform.unselect("tempo", "allegro")
    assert webform._formdata == MultiDict(  # type: ignore
        [
            ("tempo", "moderato"),
        ]
    )


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param(
            """<form></form>""",
            '"tempo" does not exists',
            id="missing-select",
        ),
        pytest.param(
            """
            <form>
                <select name="tempo" multiple>
                    <option>piano</option>
                    <option selected>moderato</option>
                </select>
            </form>
            """,
            'No option allegro in <select name="tempo">',
            id="missing-option",
        ),
        pytest.param(
            """
            <form>
                <select name="tempo" multiple>
                    <option>allegro</option>
                    <option selected>moderato</option>
                </select>
            </form>
            """,
            '"allegro" not selected in "tempo"',
            id="option-not-selected",
        ),
        pytest.param(
            """
            <form>
                <input name="tempo" type="checkbox" value="moderato" />
            </form>
            """,
            "tempo is a <input>, use unset() for checkbox instead",
            id="input",
        ),
        pytest.param(
            """
            <form>
                <select name="tempo">
                    <option>piano</option>
                    <option selected>moderato</option>
                </select>
            </form>
            """,
            "only <select multiple> support unselect",
            id="select-not-multiple",
        ),
    ],
)
def test_unselect_exception(webform: WebForm, expected: str):
    with pytest.raises(ValueError) as ctx:
        webform.unselect("tempo", "allegro")
    assert str(ctx.value) == expected


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
