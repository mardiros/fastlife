from typing import Optional

from .base import Widget


class TextWidget(Widget[str]):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        hint: Optional[str] = None,
        aria_label: Optional[str] = None,
        placeholder: Optional[str] = None,
        error: str | None = None,
        removable: bool = False,
        value: str = "",
        token: Optional[str] = None,
        input_type: str = "text",
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
        return "pydantic_form.Text"


class TextareaWidget(Widget[str]):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        hint: Optional[str] = None,
        aria_label: Optional[str] = None,
        placeholder: Optional[str] = None,
        error: str | None = None,
        removable: bool = False,
        value: str = "",
        token: Optional[str] = None,
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

    def get_template(self) -> str:
        return "pydantic_form.Textarea"
