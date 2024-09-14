from pathlib import Path
from typing import Iterator

import bs4
import pytest

from fastlife.templating.renderer.jinjax import JinjaxRenderer


@pytest.fixture(scope="module")
def tmp_dir(components_dir: Path) -> Iterator[Path]:
    ret = components_dir / "t"
    ret.mkdir(exist_ok=True)
    yield ret
    ret.rmdir()


@pytest.fixture()
def node(
    renderer: JinjaxRenderer, template_string: str, tmp_dir: Path
) -> Iterator[bs4.PageElement]:
    component = tmp_dir / "X.jinja"
    component.write_text(template_string)
    try:
        res = renderer.render_template("t.X")
        bsoup = bs4.BeautifulSoup(res, features="html.parser")
        yield next(bsoup.children)  # type: ignore
    except Exception as exc:
        # Display the error in the assertion is a compromise
        yield exc  # type: ignore
    component.unlink()


@pytest.fixture()
def expected(expected_string: str) -> bs4.PageElement:
    expected_soup = bs4.BeautifulSoup(expected_string, features="html.parser")
    return next(expected_soup.children)  # type: ignore


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<A href="/" :disable-htmx="true">Oh</A>""",
            """<a href="/" class="text-primary-600 hover:text-primary-500
            hover:underline dark:text-primary-300 dark:hover:text-primary-400"
            >Oh</a>""",
            id="A-hx-disabled",
        ),
        pytest.param(
            """<A href="/" class="css" :disable-htmx="true">Oh</A>""",
            """<a href="/" class="css">Oh</a>""",
            id="A-class",
        ),
        pytest.param(
            """<A href="/" class="css">Oh</A>""",
            """<a href="/" class="css" href="/" hx-get="/" hx-push-url="true"
                hx-swap="innerHTML show:body:top"
                hx-target="#maincontent">Oh</a>""",
            id="A-hx-enabled",
        ),
        pytest.param(
            """<A href="/" class="css" hx-target="body" hx-swap="outerHTML"
            :hx-push-url="false">Ah</A>""",
            """<a href="/" class="css" href="/" hx-get="/" hx-swap="outerHTML"
            hx-target="body">Ah</a>""",
            id="A-hx-params",
        ),
        pytest.param(
            """<A href="/" class="css" hx-target="#nav" hx-select="#nav">Ah</A>""",
            """<a href="/" class="css" hx-target="#nav" hx-select="#nav"
            hx-get="/" hx-push-url="true" hx-swap="innerHTML show:body:top">Ah</a>""",
            id="A-hx-select",
        ),
    ],
)
def test_render_A(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Button>Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="bg-primary-600 px-5 py-2.5 font-semibold rounded-lg text-center
            text-sm text-white hover:bg-primary-700 hover:bg-primary-200
            focus:outline-none focus:ring-4 focus:ring-primary-300 dark:bg-primary-600
            dark:focus:ring-primary-800 dark:hover:bg-primary-700"
            >Go</button>""",
            id="button",
        ),
        pytest.param(
            """<Button class="css">Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="css">Go</button>""",
            id="button-css",
        ),
        pytest.param(
            """<Button class="css" :full-width="true">Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="w-full css">Go</button>""",
            id="button-css-full-width",
        ),
        pytest.param(
            """<Button class="css" :hidden="true">Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="css" hidden>Go</button>""",
            id="button-hidden",
        ),
        pytest.param(
            """<Button class="css" id="gg" name="act" value="get"
            aria-label="goto">Go</Button>""",
            """<button name="act" id="gg" type="submit" value="get"
            aria-label="goto" class="css">Go</button>""",
            id="button-params",
        ),
        pytest.param(
            """<Button onclick="javascript:x()" class="css">Go</Button>""",
            """<button onclick="javascript:x()" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-onclick",
        ),
        pytest.param(
            """<Button hx-target="#body" hx-swap="body top"
            hx-get="/" hx-select="#body" hx-after_request=""
            hx-vals='{"a":"A"}' class="css">Go</Button>""",
            """<button hx-get="/" hx-select="#body"
            hx-swap="body top" hx-target="#body" hx-vals='{"a":"A"}'
            name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-params",
        ),
        pytest.param(
            """<Button hx-get="/" :hx-push-url="true" class="css">Go</Button>""",
            """<button hx-get="/" hx-push-url="true" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-disable-push-url",
        ),
        pytest.param(
            """<Button hx-post="/" hx-params="none" class="css">Go</Button>""",
            """<button hx-post="/" hx-params="none" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-disable-push-url",
        ),
        pytest.param(
            """<Button hx-put="/" hx-params="none" class="css">Go</Button>""",
            """<button hx-put="/" hx-params="none" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-disable-push-url",
        ),
        pytest.param(
            """<Button hx-patch="/" hx-params="none" class="css">Go</Button>""",
            """<button hx-patch="/" hx-params="none" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-disable-push-url",
        ),
        pytest.param(
            """<Button hx-delete="/" hx-params="none" class="css">Go</Button>""",
            """<button hx-delete="/" hx-params="none" name="action" type="submit"
            value="submit" class="css">Go</button>""",
            id="button-hx-disable-push-url",
        ),
    ],
)
def test_render_Button(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Checkbox id="foo-bar" name="foo" :checked="true" />""",
            """<input type="checkbox" id="foo-bar" name="foo" checked
            class="bg-neutral-100 border-neutral-300 h-4 rounded text-primary-600
            w-4 dark:bg-neutral-700 dark:border-neutral-600 dark:focus:ring-primary-600
            dark:ring-offset-neutral-800 focus:ring-2 focus:ring-primary-500"/>""",
            id="checkbox-checked",
        ),
        pytest.param(
            """<Checkbox id="foo-bar" name="foo" class="css"/>""",
            """<input type="checkbox" id="foo-bar" name="foo" class="css"/>""",
            id="checkbox-css",
        ),
        pytest.param(
            """<Checkbox id="foo-bar" name="foo" value="bar" checked class="css"/>""",
            """<input type="checkbox" id="foo-bar" name="foo" value="bar" checked
            class="css"/>""",
            id="checkbox-checked-value",
        ),
    ],
)
def test_render_Checkbox(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<CsrfToken />""",
            """<input type="hidden" name="csrf_token" value=""/>""",
            id="csrf",
        ),
    ],
)
def test_render_CSRFToken(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Form>XxX</Form>""",
            """<form class="space-y-4 md:space-y-6">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form",
        ),
        pytest.param(
            """<Form class="form">XxX</Form>""",
            """<form class="form">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form-css",
        ),
        pytest.param(
            """<Form class="form" action="" method="post">XxX</Form>""",
            """<form class="form" action="" method="post">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form-post",
        ),
        pytest.param(
            """<Form class="form" hx-post>XxX</Form>""",
            """<form class="form" hx-post="">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form-hx-post",
        ),
        pytest.param(
            """<Form hx-post="/go" class="form">XxX</Form>""",
            """<form class="form" hx-post="/go">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form-hx-post-url",
        ),
        pytest.param(
            """<Form method="get" hx-post="/go" class="form">XxX</Form>""",
            """<form class="form" hx-post="/go" method="get">
  <input name="csrf_token" type="hidden" value=""/>XxX</form>""",
            id="form-hx-get",
        ),
    ],
)
def test_render_Form(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H1(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H2(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H3(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H4(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H5(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_H6(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Hidden name="key" value="val"/>""",
            """<input name="key" value="val" type="hidden" />""",
            id="Hidden",
        ),
        pytest.param(
            """<Hidden id="k" name="key" value="val"/>""",
            """<input id="k" name="key" value="val" type="hidden" />""",
            id="Hidden-id",
        ),
    ],
)
def test_render_Hidden(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Input name="key" value="val"/>""",
            """<input name="key" value="val" type="text" class="bg-neutral-50 block
            border border-neutral-300 p-2.5 rounded-lg text-base text-neutral-900
            w-full dark:bg-neutral-700 dark:border-neutral-600
            dark:focus:border-primary-500 dark:focus:ring-primary-500
            dark:placeholder-neutral-400 dark:text-white focus:border-primary-500
            focus:ring-primary-500" />""",
            id="Input",
        ),
        pytest.param(
            """<Input id="k" name="key" value="val" class="x" />""",
            """<input id="k" name="key" value="val" type="text" class="x" />""",
            id="Input-id-css",
        ),
    ],
)
def test_render_Input(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Label for="y">yoyo</Label>""",
            """<label class="block font-bold mb-2 text-base text-neutral-900
                             dark:text-white"
                        for="y">yoyo</label>""",
            id="label",
        ),
        pytest.param(
            """<Label class="foo" for="bar">barbar</Label>""",
            """<label class="foo" for="bar">barbar</label>""",
            id="label-class",
        ),
    ],
)
def test_render_Label(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Option value="y">yoyo</Option>""",
            """<option value="y">yoyo</option>""",
            id="option",
        ),
        pytest.param(
            """<Option value="y" :selected="true">yoyo</Option>""",
            """<option value="y" selected>yoyo</option>""",
            id="option-selected",
        ),
    ],
)
def test_render_Option(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


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
def test_render_P(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Radio label="lbl" id="radio-id" name="radio-name" value="val" />""",
            """<div class="flex items-center mb-4">
  <input type="radio" name="radio-name" value="val" id="radio-id" class="bg-neutral-100
  border-neutral-300 w-4 h-4 text-primary-600 focus:ring-2 focus:ring-primary-500
  dark:bg-neutral-700 dark:border-neutral-600 dark:focus:ring-primary-600
  dark:ring-offset-neutral-800">
  <label for="radio-id" class="dark:text-neutral-300 font-medium ms-2
  text-neutral-900 text-sm">lbl</label>
</div>
""",
            id="radio",
        ),
        pytest.param(
            """<Radio label="lbl" id="radio-id" name="radio-name" value="val"
            class="radio" label-class="lbl" div-class="d" />""",
            """<div class="d">
  <input type="radio" name="radio-name" value="val" id="radio-id" class="radio">
  <label for="radio-id" class="lbl">lbl</label>
</div>
""",
            id="radio-css",
        ),
    ],
)
def test_render_Radio(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Select name="n" id="i">X</Select>""",
            """<select name="n" id="i" class="bg-neutral-50 block border
            border-neutral-300 p-2.5 rounded-lg text-base text-neutral-900
            w-full focus:border-primary-500 focus:ring-primary-500
            dark:bg-neutral-700 dark:border-neutral-600
            dark:focus:border-primary-500
            dark:focus:ring-primary-500 dark:placeholder-neutral-400
            dark:text-white">X</select>""",
            id="select",
        ),
        pytest.param(
            """<Select name="n" id="i" class="slct">X</Select>""",
            """<select name="n" id="i" class="slct">X</select>""",
            id="select-css",
        ),
        pytest.param(
            """<Select name="n" id="i" class="slct" multiple>X</Select>""",
            """<select name="n" id="i" class="slct" multiple>X</select>""",
            id="select-multiple",
        ),
    ],
)
def test_render_Select(node: bs4.PageElement, expected: bs4.PageElement):
    assert node == expected
