"""Class utilities to access to the web form."""

from typing import TYPE_CHECKING, Any

from multidict import MultiDict

if TYPE_CHECKING:
    from .dom import Element  # coverage: ignore
    from .testclient import WebResponse, WebTestClient  # coverage: ignore


class WebForm:
    """
    Handle html form.

    Form are filled out and submit with methods and try to avoid invalid
    usage, such as selecting an option that don't exists is not possible here.
    Again, no javascript is executed here, but htmx attribute `hx-post` and `hx-target`
    are read while submiting to simulate it.
    """

    def __init__(self, client: "WebTestClient", origin: str, form: "Element"):
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
            raise ValueError(f"{fieldname} is a {field!r}, use set() instead")

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
