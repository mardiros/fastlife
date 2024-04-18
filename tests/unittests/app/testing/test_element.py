import pytest

from fastlife.testing.testclient import Element


@pytest.mark.parametrize("html", ["<a href='/'>click me</a>"])
def test_click(element: Element):
    resp = element.click()
    assert resp.html.h1.text == "Hello World!"


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<p>paragraph</p>", "p"),
        ("<a href='/'>click me</a>", "a"),
        ("<p>paragraph <a href='/'>click me</a></p>", "p"),
    ],
)
def test_node_name(element: Element, expected: str):
    assert element.node_name == expected


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<p id='p1' class='para'>paragraph</p>", {"id": "p1", "class": ["para"]}),
        ("<a id='link' href='/'>click me</a>", {"id": "link", "href": "/"}),
    ],
)
def test_attrs(element: Element, expected: dict[str, str]):
    assert element.attrs == expected


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<p>paragraph</p>", "paragraph"),
        ("<p> paragraph </p>", "paragraph"),
        ("<p>\tparagraph\n</p>", "paragraph"),
        ("<p>paragraph <a href='/'>click me</a></p>", "paragraph click me"),
        ("<p>paragraph \n<a href='/'>click me</a>\n</p>", "paragraph \nclick me"),
    ],
)
def test_text(element: Element, expected: str):
    assert element.text == expected


@pytest.mark.parametrize(
    "html",
    [
        "<div><h1>I am the one</h1></div>",
        "<div><h1>I am the one</h1><h2>ii</h2><h2>iii</h2></div>",
    ],
)
def test_h1(element: Element):
    assert element.h1.text == "I am the one"


@pytest.mark.parametrize(
    "html",
    [
        "<div><h1>I am the one</h1><h1>Sorry</h1></div>",
    ],
)
def test_h1_many_raises(element: Element):
    with pytest.raises(AssertionError) as ctx:
        element.h1.text
    assert (
        str(ctx.value)
        == "Should have 1 <h1>, got 2 in <div><h1>I am the one</h1><h1>Sorry</h1></div>"
    )


@pytest.mark.parametrize(
    "html",
    [
        "<div><h1>I am the one</h1><h2>ii</h2><h3>ii-a</h3><h2>iii</h2></div>",
    ],
)
def test_h2(element: Element):
    assert [h.text for h in element.h2] == ["ii", "iii"]


@pytest.mark.parametrize("html", ["<div><p>paragraph</p></div>"])
def test_form_is_none(element: Element):
    assert element.form is None


@pytest.mark.parametrize(
    "html",
    [
        "<div><form action='/' method='post'><input type='text' name='h'></form></div>",
    ],
)
def test_form(element: Element):
    assert element.form is not None
    assert element.form.node_name == "form"
    assert element.form.attrs == {"action": "/", "method": "post"}


@pytest.mark.parametrize(
    "html",
    [
        "<form action='/' hx-target='mybody'><input type='text' name='h'></form>",
    ],
)
def test_hx_target(element: Element):
    assert element.hx_target is not None
    assert element.hx_target == "mybody"


@pytest.mark.parametrize(
    "html",
    [
        "<form action='/'><input type='text' name='h'></form>",
    ],
)
def test_hx_target_is_none(element: Element):
    assert element.hx_target is None


@pytest.mark.parametrize(
    "html",
    [
        "<form action='/' hx-target='buddy'><button type='button'>X</button></form>",
    ],
)
def test_hx_target_in_parent(element: Element):
    button = element.by_node_name("button")[0]
    assert button.hx_target is not None
    assert button.hx_target == "buddy"


@pytest.mark.parametrize(
    "html",
    [
        "<div><h1>I am the one</h1><h2>ii</h2><h3>ii-a</h3><h2>iii</h2></div>",
        "<div><h1>I am the one</h1><h2>ii</h2><h3>ii-a</h3><p>ii-a</p></div>",
    ],
)
def test_by_text(element: Element):
    h3 = element.by_text("ii-a")
    assert h3 is not None
    assert h3.node_name == "h3"


@pytest.mark.parametrize(
    "html,expected",
    [
        (
            "<div><h1>I am the one</h1><h2>ii</h2><h3>ii-a</h3><h2>iii</h2></div>",
            ["h3"],
        ),
        (
            "<div><h1>I am the one</h1><h2>ii</h2><h3>ii-a</h3><p>ii-a</p></div>",
            ["h3", "p"],
        ),
    ],
)
def test_get_all_by_text(element: Element, expected: str):
    alls = element.get_all_by_text("ii-a")
    assert [i.node_name for i in alls] == expected


@pytest.mark.parametrize(
    "html",
    [
        """
            <form>
                <label for="my-target">fetch target</label>
                <input type="text" id="my-target">
            </form>
        """,
        """
            <form>
                <label for="my-target">fetch target</label>
                <input type="text" id="my-target">
                <input type="text" id="could-it-be">
            </form>
        """,
    ],
)
def test_by_label_text(element: Element):
    target = element.by_label_text("fetch target")
    assert target is not None
    assert target.attrs["id"] == "my-target"


@pytest.mark.parametrize(
    "html",
    [
        """
            <form>
                <label for="my-target">fetch target</label>
                <input type="text" id="could-it-be">
            </form>
        """,
    ],
)
def test_by_label_text_not_found(element: Element):
    target = element.by_label_text("fetch target")
    assert target is None


@pytest.mark.parametrize(
    "html",
    [
        """
            <form>
                <label for="my-target">fetch target</label>
                <input type="text" id="my-target">
                <fieldset>
                    <label for="could-it-be">another target</label>
                    <input type="text" id="could-it-be">
                </fieldset>
            </form>
        """,
    ],
)
def test_by_node_name(element: Element):
    target = element.by_node_name("label")
    assert len(target) == 2
    assert target[0].attrs["for"] == "my-target"
    assert target[1].attrs["for"] == "could-it-be"

    target = element.by_node_name("label", attrs={"for": "could-it-be"})
    assert len(target) == 1
    assert target[0].text == "another target"


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<div><h1>I am the one</h1></div>", "<div>"),
        ("<h1>I am the one</h1>", "<h1>"),
        ("<h1 id='woot'>I am the one</h1>", "<h1>"),
    ],
)
def test_repr(element: Element, expected: str):
    assert repr(element) == expected


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<div><h1>I am the one</h1></div>", "<div><h1>I am the one</h1></div>"),
    ],
)
def test_str(element: Element, expected: str):
    assert str(element) == expected
