import pytest
from bs4 import PageElement

button_css = (
    "appearance-none bg-primary-600 px-5 py-2.5 font-semibold rounded-lg "
    "text-center text-sm text-white hover:bg-primary-700 "
    "hover:bg-primary-200 focus:outline-hidden focus:ring-4 focus:ring-primary-300 "
    "dark:bg-primary-600 dark:focus:ring-primary-800 dark:hover:bg-primary-700"
)


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Button>Go</Button>""",
            f"""
            <button name="action" type="submit" value="submit"
                    class="{button_css}"
                    >Go</button>
            """,
            id="default",
        ),
        pytest.param(
            """<Button class="css">Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="css">Go</button>""",
            id="button-css",
        ),
        pytest.param(
            """<Button class="css" full-width={true}>Go</Button>""",
            """<button name="action" type="submit" value="submit"
            class="w-full css">Go</button>""",
            id="button-css-full-width",
        ),
        pytest.param(
            """<Button class="css" hidden={true}>Go</Button>""",
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
            hx-get="/" hx-select="#body"
            hx-vals='{"a":"A"}' class="css">Go</Button>""",
            """
            <button hx-get="/" hx-select="#body" hx-swap="body top" hx-target="#body"
            hx-vals='{"a":"A"}'
            name="action" type="submit" value="submit" class="css">Go</button>""",
            id="button-hx-params",
        ),
    ],
)
def test_Button(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Checkbox id="foo-bar" name="foo" checked={true} />""",
            """<input type="checkbox" id="foo-bar" name="foo" checked
            class="bg-neutral-100 border-neutral-300 h-4 rounded-sm text-primary-600
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
def test_render_Checkbox(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<CsrfToken />""",
            """<input type="hidden" name="csrf_token" value="CsRfT"/>""",
            id="csrf",
        ),
    ],
)
def test_render_CSRFToken(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Form>XxX</Form>""",
            """<form class="space-y-4 md:space-y-6"><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form",
        ),
        pytest.param(
            """<Form class="form">XxX</Form>""",
            """<form class="form"><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form-css",
        ),
        pytest.param(
            """<Form class="form" action="" method="post">XxX</Form>""",
            """<form class="form" action="" method="post"><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form-post",
        ),
        pytest.param(
            """<Form class="form" hx-post>XxX</Form>""",
            """<form class="form" hx-post=""><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form-hx-post",
        ),
        pytest.param(
            """<Form hx-post="/go" class="form">XxX</Form>""",
            """<form class="form" hx-post="/go"><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form-hx-post-url",
        ),
        pytest.param(
            """<Form method="get" hx-post="/go" class="form">XxX</Form>""",
            """<form class="form" hx-post="/go" method="get"><input name="csrf_token" type="hidden" value="CsRfT"/>XxX</form>""",
            id="form-hx-get",
        ),
    ],
)
def test_render_Form(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


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
def test_render_Hidden(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


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
        pytest.param(
            """<Input name="key" value="" class="x" inputmode="tel" />""",
            """<input name="key" value="" type="text" inputmode="tel" class="x" />""",
            id="Input-inputmode",
        ),
        pytest.param(
            """<Input name="key" value="" class="x"
                autocomplete="new-password" />""",
            """<input name="key" value="" type="text"
                autocomplete="new-password" class="x" />""",
            id="Input-autocomplete",
        ),
        pytest.param(
            """<Input name="key" value="" class="x" autofocus={true} />""",
            """<input name="key" value="" type="text" class="x" autofocus/>""",
            id="Input-autofocus",
        ),
    ],
)
def test_render_Input(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Password name="key" />""",
            """<input name="key" type="password" class="bg-neutral-50 block
                border border-neutral-300 p-2.5 rounded-lg text-base text-neutral-900
                w-full dark:bg-neutral-700 dark:border-neutral-600
                dark:focus:border-primary-500 dark:focus:ring-primary-500
                dark:placeholder-neutral-400 dark:text-white focus:border-primary-500
                focus:ring-primary-500" />""",
            id="Password",
        ),
        pytest.param(
            """<Password id="k" name="key" type="password" class="x" />""",
            """<input id="k" name="key" type="password" class="x" />""",
            id="Password-id-css",
        ),
        pytest.param(
            """<Password name="pin" class="x" inputmode="tel"
                minlength="8" minlength="42" pattern="[a-zA-Z0-9]+"/>""",
            """<input name="pin" type="password" inputmode="tel"
                minlength="8" minlength="42" pattern="[a-zA-Z0-9]+" class="x" />""",
            id="Input-attrs",
        ),
        pytest.param(
            """<Password name="key" class="x" autocomplete="new-password" />""",
            """<input name="key" type="password"
                autocomplete="new-password" class="x" />""",
            id="Input-autocomplete",
        ),
        pytest.param(
            """<Password name="key" class="x" autofocus={true} />""",
            """<input name="key" type="password" class="x" autofocus/>""",
            id="Input-autofocus",
        ),
    ],
)
def test_render_Password(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


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
def test_render_Label(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Option value="y">yoyo</Option>""",
            """<option value="y">yoyo</option>""",
            id="option",
        ),
        pytest.param(
            """<Option value="y" selected={true}>yoyo</Option>""",
            """<option value="y" selected>yoyo</option>""",
            id="option-selected",
        ),
    ],
)
def test_render_Option(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


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
def test_render_Select(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """<Radio label="lbl" id="radio-id" name="radio-name" value="val" />""",
            """<div class="flex items-center mb-4"><input type="radio"
            name="radio-name" value="val" id="radio-id" class="bg-neutral-100
            border-neutral-300 w-4 h-4 text-primary-600 focus:ring-2
            focus:ring-primary-500 dark:bg-neutral-700 dark:border-neutral-600
            dark:focus:ring-primary-600 dark:ring-offset-neutral-800"><label
            for="radio-id" class="ms-2 text-sm font-medium text-neutral-900
            dark:text-neutral-300">lbl</label></div>
            """,
            id="default",
        ),
        pytest.param(
            """<Radio label="lbl" id="radio-id" name="radio-name" value="val"
            class="radio" label-class="lbl" div-class="d" />""",
            """<div class="d"><input type="radio" name="radio-name" value="val"
            id="radio-id" class="radio"><label for="radio-id"
            class="lbl">lbl</label></div>
            """,
            id="css",
        ),
    ],
)
def test_render_Radio(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """
            <Textarea name="text">
                The quick brown fox jumps over the lazy dog
            </Textarea>""",
            """
            <textarea name="text" class="bg-neutral-50 block border
            border-neutral-300 p-2.5 rounded-lg text-base text-neutral-900
            w-full dark:bg-neutral-700 dark:border-neutral-600
            dark:focus:border-primary-500 dark:focus:ring-primary-500
            dark:placeholder-neutral-400 dark:text-white focus:border-primary-500
            focus:ring-primary-500">
                The quick brown fox jumps over the lazy dog
            </textarea>
            """,
            id="default",
        ),
        pytest.param(
            """
            <Textarea name="text" id="texta" class="texty">
                The quick brown fox jumps over the lazy dog
            </Textarea>""",
            """
            <textarea name="text" id="texta" class="texty">
                The quick brown fox jumps over the lazy dog
            </textarea>
            """,
            id="css",
        ),
    ],
)
def test_render_Textarea(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
