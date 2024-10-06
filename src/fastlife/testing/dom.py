"""Class utilities to access to the DOM."""

import re
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any

import bs4
from multidict import MultiDict

if TYPE_CHECKING:
    from .testclient import WebResponse, WebTestClient  # coverage: ignore


class Element:
    """Access to a dom element."""

    def __init__(self, client: "WebTestClient", tag: bs4.Tag):
        self._client = client
        self._tag = tag

    def click(self) -> "WebResponse":
        """Simulate a client to a a link. No javascript exectuted here."""
        return self._client.get(self._tag.attrs["href"])

    @property
    def node_name(self) -> str:
        """Get the node name of the dom element."""
        return self._tag.name

    @property
    def attrs(self) -> dict[str, str]:
        """Attributes of the element."""
        return self._tag.attrs

    @property
    def text(self) -> str:
        """
        Return the text of the element, with text of childs element.

        Note that the text is stripped for convenience but inner text may contains
        many spaces not manipulated here.
        """
        return self._tag.text.strip()

    @property
    def h1(self) -> "Element":
        """
        Return the h1 child element.

        Should be used on the html body element directly.
        """
        nodes = self.by_node_name("h1")
        assert len(nodes) == 1, f"Should have 1 <h1>, got {len(nodes)} in {self}"
        return nodes[0]

    @property
    def h2(self) -> Sequence["Element"]:
        """
        Return the h2 elements.
        """
        return self.by_node_name("h2")

    @property
    def form(self) -> "Element | None":
        """Get the form element of the web page."""
        return Element(self._client, self._tag.form) if self._tag.form else None

    @property
    def hx_target(self) -> str | None:
        """
        Return the hx-target of the element.

        It may be set on a parent. It also resolve special case "this" and return the id
        of the element.
        """
        el: bs4.Tag | None = self._tag
        while el:
            if "hx-target" in el.attrs:
                ret = el.attrs["hx-target"]
                if ret == "this":
                    ret = el.attrs["id"]
                return ret
            el = el.parent
        return None

    def by_text(self, text: str, *, node_name: str | None = None) -> "Element | None":
        """Find the first element that match the text."""
        nodes = self.iter_all_by_text(text, node_name=node_name)
        return next(nodes, None)

    def iter_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Iterator[Element]":
        """Return an iterator of all elements that match the text."""
        nodes = self._tag.find_all(string=re.compile(rf"\s*{text}\s*"))
        for node in nodes:
            if isinstance(node, bs4.NavigableString):
                node = node.parent

            if node_name:
                while node is not None:
                    if node.name == node_name:
                        yield Element(self._client, node)
                    node = node.parent
            elif node:
                yield Element(self._client, node)
        return None

    def get_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Sequence[Element]":
        """Return the list of all elements that match the text."""
        nodes = self.iter_all_by_text(text, node_name=node_name)
        return list(nodes)

    def by_label_text(self, text: str) -> "Element | None":
        """Return the element which is the target of the label having the given text."""
        label = self.by_text(text, node_name="label")
        assert label is not None
        assert label.attrs.get("for") is not None
        resp = self._tag.find(id=label.attrs["for"])
        assert not isinstance(resp, bs4.NavigableString)
        return Element(self._client, resp) if resp else None

    def by_node_name(
        self, node_name: str, *, attrs: dict[str, str] | None = None
    ) -> list["Element"]:
        """
        Return the list of elements with the given node_name.

        An optional set of attributes may given and must match if passed.
        """
        return [
            Element(self._client, e) for e in self._tag.find_all(node_name, attrs or {})
        ]

    def __repr__(self) -> str:
        return f"<{self.node_name}>"

    def __str__(self) -> str:
        return str(self._tag)


class WebForm:
    """
    Handle html form.

    Form are filled out and submit with methods and try to avoid invalid
    usage, such as selecting an option that don't exists is not possible here.
    Again, no javascript is executed here, but htmx attribute `hx-post` and `hx-target`
    are read while submiting to simulate it.
    """

    def __init__(self, client: "WebTestClient", origin: str, form: Element):
        self._client = client
        self._form = form
        self._origin = origin
        self._formfields: dict[str, Element] = {}
        self._formdata: MultiDict[str] = MultiDict()
        inputs = self._form.by_node_name("input")
        for input in inputs:
            self._formfields[input.attrs["name"]] = input
            if input.attrs.get("type") == "checkbox" and "checked" not in input.attrs:
                continue
            self._formdata.add(input.attrs["name"], input.attrs.get("value", ""))

        selects = self._form.by_node_name("select")
        for select in selects:
            fieldname = select.attrs["name"]
            self._formfields[fieldname] = select
            options = select.by_node_name("option")
            if "multiple" in select.attrs:
                for option in options:
                    if "selected" in option.attrs:
                        self._formdata.add(
                            fieldname, option.attrs.get("value", option.text)
                        )
            else:
                if options:
                    self._formdata[fieldname] = options[0].attrs.get(
                        "value", options[0].text
                    )
                    for option in options:
                        if "selected" in option.attrs:
                            self._formdata[fieldname] = option.attrs.get(
                                "value", option.text
                            )
                            break

        # field textearea...

    def set(self, fieldname: str, value: str) -> Any:
        """
        Set a value to an input field.

        It works for checkbox and radio as well.
        Checkbox may contains many values.
        Options of select can't be set with this method, the select method must
        be used instead.
        """
        if fieldname not in self._formfields:
            raise ValueError(f'"{fieldname}" does not exists')
        if self._formfields[fieldname].node_name == "select":
            raise ValueError(f'"{fieldname}" is a <select>, use select() instead')

        if self._formfields[fieldname].attrs.get("type") == "checkbox":
            self._formdata.add(fieldname, value)
            return

        if self._formfields[fieldname].attrs.get("type") == "radio":
            radio = self._form.by_node_name(
                "input", attrs={"type": "radio", "value": value}
            )
            if not radio:
                raise ValueError(
                    f'radio "{fieldname}" does not contains {value} option'
                )

        self._formdata[fieldname] = value

    def unset(self, fieldname: str, value: str) -> Any:
        """Unset an element. Only works with checkbox."""
        if fieldname not in self._formfields:
            raise ValueError(f'"{fieldname}" does not exists')
        if self._formfields[fieldname].node_name != "input":
            raise ValueError(f'"{fieldname}" is not a checkbox')
        if self._formfields[fieldname].attrs.get("type") != "checkbox":
            raise ValueError(f'"{fieldname}" is not a checkbox')
        values = self._formdata.popall(fieldname)
        if value not in values:
            raise ValueError(f'"{value}" not in "{fieldname}"')
        for val in values:
            if val != value:
                self._formdata[fieldname] = val

    def select(self, fieldname: str, value: str) -> Any:
        """
        Select an option, if multiple, value is added, otherwise, value is replaced.
        """
        if fieldname not in self._formfields:
            raise ValueError(f'"{fieldname}" does not exists')
        field = self._formfields[fieldname]
        if field.node_name != "select":
            raise ValueError(f"{fieldname} is a {field!r}, " "use set() instead")

        for option in field.by_node_name("option"):
            if option.text == value.strip():
                if "multiple" in field.attrs:
                    self._formdata.add(fieldname, value)
                else:
                    self._formdata[fieldname] = option.attrs.get("value", option.text)
                break
        else:
            raise ValueError(f'No option {value} in <select name="{fieldname}">')

    def unselect(self, fieldname: str, value: str) -> Any:
        """
        Unselect an option if multiple, otherwise an exception is raised.
        """
        if fieldname not in self._formfields:
            raise ValueError(f'"{fieldname}" does not exists')
        field = self._formfields[fieldname]

        if field.node_name != "select":
            raise ValueError(
                f"{fieldname} is a {self._formfields[fieldname]!r}, "
                "use unset() for checkbox instead"
            )
        if "multiple" not in field.attrs:
            raise ValueError("only <select multiple> support unselect")

        for option in self._formfields[fieldname].by_node_name("option"):
            if option.text == value.strip():
                values = self._formdata.popall(fieldname)
                if value not in values:
                    raise ValueError(f'"{value}" not selected in "{fieldname}"')
                for val in values:
                    if val != value:
                        self._formdata[fieldname] = val
                break
        else:
            raise ValueError(f'No option {value} in <select name="{fieldname}">')

    def button(self, text: str, position: int = 0) -> "WebForm":
        """
        Simmulate a click on a button using the text of the button,

        and eventually a position. The button return the form and the submit()
        should be called directly.

        This is used in order to inject the value of the button in the form, usually
        done while many actions are available on a form.

        ::

            form.button("Go").submit()

        """
        buttons = self._form.get_all_by_text(text, node_name="button")
        if position >= len(buttons):
            pos = ""
            if position > 0:
                pos = f" at position {position}"
            raise ValueError(f'Button "{text}" not found{pos}')
        button = buttons[position]
        if "name" in button.attrs:
            self._formdata[button.attrs["name"]] = button.attrs.get("value", "")
        return self

    def submit(self, follow_redirects: bool = True) -> "WebResponse":
        """
        Submit the form as it has been previously filled out.
        """
        headers: dict[str, str] = {}
        target = (
            self._form.attrs.get("hx-post")
            or self._form.attrs.get("post")
            or self._origin
        )
        if "hx-post" in self._form.attrs:
            if hx_target := self._form.hx_target:
                headers["HX-Target"] = hx_target

        return self._client.post(
            target,
            data=self._formdata,
            headers=headers,
            follow_redirects=follow_redirects,
        )

    def __contains__(self, key: str) -> bool:
        """Test if a field exists in the form."""
        return key in self._formdata

    def __repr__(self) -> str:
        return repr(self._formdata)
