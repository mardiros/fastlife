"""
Widget for field of type Set.
"""

from collections.abc import Sequence

from pydantic import BaseModel, Field

from .base import Widget


class Checkable(BaseModel):
    """A checkable field from a checklist."""

    label: str
    name: str
    value: str
    token: str
    checked: bool
    error: str | None = Field(default=None)

    @property
    def id(self) -> str:
        id = f"{self.name}-{self.value}-{self.token}"
        return id.replace(".", "-").replace("_", "-")

    @property
    def field_name(self) -> str:
        return f"{self.name}[]"


class ChecklistWidget(Widget[Sequence[Checkable]]):
    """
    Widget for field of type Set.

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
        value: Sequence[Checkable],
        error: str | None = None,
        token: str,
        removable: bool,
    ) -> None:
        super().__init__(
            name,
            value=value,
            error=error,
            token=token,
            title=title,
            hint=hint,
            aria_label=aria_label,
            removable=removable,
        )

    def get_template(self) -> str:
        return "pydantic_form.Checklist.jinja"
