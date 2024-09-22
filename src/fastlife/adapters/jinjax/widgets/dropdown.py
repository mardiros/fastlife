"""
Widget for field of type Enum or Literal.
"""

from typing import Optional, Sequence, Tuple

from .base import Widget


class DropDownWidget(Widget[str]):
    """
    Widget for field of type Enum or Literal.

    :param name: field name.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param value: current value.
    :param error: error of the value if any.
    :param options: List of possible values.
    :param removable: display a button to remove the widget for optional fields.
    :param token: token used to get unique id on the form.
    """

    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        hint: Optional[str] = None,
        aria_label: Optional[str] = None,
        value: Optional[str] = None,
        error: str | None = None,
        options: Sequence[Tuple[str, str]] | Sequence[str],
        removable: bool = False,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(
            name,
            value=value,
            error=error,
            title=title,
            token=token,
            removable=removable,
            hint=hint,
            aria_label=aria_label,
        )
        self.options: list[dict[str, str]] = []
        for opt in options:
            if isinstance(opt, tuple):
                self.options.append({"value": opt[0], "text": opt[1]})
            else:
                self.options.append({"value": opt, "text": opt})

    def get_template(self) -> str:
        return "pydantic_form.Dropdown.jinja"
