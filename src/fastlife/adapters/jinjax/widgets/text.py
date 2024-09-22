from collections.abc import Sequence
from typing import Optional

from .base import Widget


class TextWidget(Widget[str]):
    """
    Widget for text like field (email, ...).

    :param name: input name.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param placeholder: html input placeholder value.
    :param error: error of the value if any.
    :param value: current value.
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
        placeholder: Optional[str] = None,
        error: str | None = None,
        value: str = "",
        input_type: str = "text",
        removable: bool = False,
        token: str,
    ) -> None:
        super().__init__(
            name,
            value=value,
            title=title,
            hint=hint,
            aria_label=aria_label,
            token=token,
            error=error,
            removable=removable,
        )
        self.placeholder = placeholder or ""
        self.input_type = input_type

    def get_template(self) -> str:
        return "pydantic_form.Text.jinja"


class TextareaWidget(Widget[Sequence[str]]):
    """
    Render a Textearea for a string or event a sequence of string.

    ```
    from fastlife.adapters.jinjax.widgets.text import TextareaWidget
    from pydantic import BaseModel, Field, field_validator

    class TaggedParagraphForm(BaseModel):
        paragraph: Annotated[str, TextareaWidget] = Field(...)
        tags: Annotated[Sequence[str], TextareaWidget] = Field(
            default_factory=list,
            title="Tags",
            description="One tag per line",
        )

        @field_validator("tags", mode="before")
        def split(cls, s: Any) -> Sequence[str]:
            return s.split() if s else []
    ```

    :param name: input name.
    :param title: title for the widget.
    :param hint: hint for human.
    :param aria_label: html input aria-label value.
    :param placeholder: html input placeholder value.
    :param error: error of the value if any.
    :param value: current value.
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
        placeholder: Optional[str] = None,
        error: str | None = None,
        value: Optional[Sequence[str]] = None,
        removable: bool = False,
        token: str,
    ) -> None:
        super().__init__(
            name,
            value=value or [],
            title=title,
            hint=hint,
            aria_label=aria_label,
            token=token,
            error=error,
            removable=removable,
        )
        self.placeholder = placeholder or ""

    def get_template(self) -> str:
        return "pydantic_form.Textarea.jinja"
