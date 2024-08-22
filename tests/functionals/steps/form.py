# type: ignore
import string
from typing import Literal

from behave import when

from tests.functionals.context import Context

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


@when('I fill the field "{label}" with "{value}"')
def fill_input(context: Context, label: str, value: str):
    field = context.browser.get_by_label(label)
    field.fill(value)


@when('I select the option "{value}" of "{label}"')
def select_option(context: Context, value: str, label: str):
    field = context.browser.get_by_label(label)
    field.select_option(value)


@when('I fill the field having the placeholder "{placeholder}" with "{value}"')
def fill_input_with_placeholder(context: Context, placeholder: str, value: str):
    field = context.browser.get_by_placeholder(placeholder)
    field.fill(value)


@when('I click on the {position} "{role}" "{name}"')
def click_element_nth(context: Context, position: str, role: Role, name: str) -> None:
    nth = int("".join([x for x in position if x in string.digits])) - 1
    element = context.browser.get_by_role(role, name=name).nth(nth)
    element.click()


@when('I click on the "{role}" "{name}"')
def click_element(context: Context, role: Role, name: str) -> None:
    element = context.browser.get_by_role(role, name=name)
    element.click()


@when('I click on the "{role}" "{name}" with response info')
def click_element_api(context: Context, role: Role, name: str) -> None:
    element = context.browser.get_by_role(role, name=name)

    with context.browser.expect_response("**") as response_info:
        element.click()
    context.response = response_info.value
