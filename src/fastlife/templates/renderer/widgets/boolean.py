"""
Widget for field of type bool.
"""

from .base import Widget


class BooleanWidget(Widget[bool]):
    """
    Widget for field of type bool.

    :param name: field name.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param value: current value.
    :param error: error of the value if any.
    :param removable: display a button to remove the widget for optional fields.
    :param token: token used to get unique id on the form.
    """

    def __init__(
        self,
        name: str,
        *,
        title: str | None,
        hint: str | None = None,
        aria_label: str | None = None,
        value: bool = False,
        error: str | None = None,
        removable: bool = False,
        token: str,
    ) -> None:
        super().__init__(
            name,
            title=title,
            hint=hint,
            aria_label=aria_label,
            value=value,
            error=error,
            removable=removable,
            token=token,
        )

    def get_template(self) -> str:
        return "pydantic_form.Boolean.jinja"
