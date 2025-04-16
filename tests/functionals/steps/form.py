import string
from typing import Any, Literal

from playwright.async_api import Page
from tursu import when

Role = Literal[
    "alert",
    "alertdialog",
    "application",
    "article",
    "banner",
    "blockquote",
    "button",
    "caption",
    "cell",
    "checkbox",
    "code",
    "columnheader",
    "combobox",
    "complementary",
    "contentinfo",
    "definition",
    "deletion",
    "dialog",
    "directory",
    "document",
    "emphasis",
    "feed",
    "figure",
    "form",
    "generic",
    "grid",
    "gridcell",
    "group",
    "heading",
    "img",
    "insertion",
    "link",
    "list",
    "listbox",
    "listitem",
    "log",
    "main",
    "marquee",
    "math",
    "menu",
    "menubar",
    "menuitem",
    "menuitemcheckbox",
    "menuitemradio",
    "meter",
    "navigation",
    "none",
    "note",
    "option",
    "paragraph",
    "presentation",
    "progressbar",
    "radio",
    "radiogroup",
    "region",
    "row",
    "rowgroup",
    "rowheader",
    "scrollbar",
    "search",
    "searchbox",
    "separator",
    "slider",
    "spinbutton",
    "status",
    "strong",
    "subscript",
    "superscript",
    "switch",
    "tab",
    "table",
    "tablist",
    "tabpanel",
    "term",
    "textbox",
    "time",
    "timer",
    "toolbar",
    "tooltip",
    "tree",
    "treegrid",
    "treeitem",
]


@when('the user fill the field "{label}" with "{value}"')
async def fill_input(page: Page, label: str, value: str):
    field = page.get_by_label(label)
    await field.fill(value)


@when('I fill the textarea "{label}" with')
async def fill_textarea(page: Page, label: str, doc_string: str):
    field = page.get_by_label(label)
    await field.fill(doc_string)


@when('I select the option "{value}" of "{label}"')
async def select_option(page: Page, value: str, label: str):
    field = page.get_by_label(label)
    await field.select_option(value)


@when('the user fill the field having the placeholder "{placeholder}" with "{value}"')
async def fill_input_with_placeholder(page: Page, placeholder: str, value: str):
    field = page.get_by_placeholder(placeholder)
    await field.fill(value)


@when('the user click on the {position} {role} "{name}"')
async def click_element_nth(page: Page, position: str, role: Role, name: str) -> None:
    nth = int("".join([x for x in position if x in string.digits])) - 1
    element = page.get_by_role(role, name=name).nth(nth)
    await element.click()


@when('the user click on the {role} "{name}"')
async def click_element(page: Page, role: Role, name: str) -> None:
    element = page.get_by_role(role, name=name)
    await element.click()


@when('the user click on the {role} "{name}" with response info')
async def click_element_api(page: Page, role: Role, name: str, response: Any) -> None:
    element = page.get_by_role(role, name=name)

    async with page.expect_response("**") as response_info:
        await element.click()
    response.set_response(response_info.value)
