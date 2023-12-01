from typing import Optional

from .base import Widget


class TextWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        aria_label: Optional[str] = None,
        placeholder: Optional[str] = None,
        removable: bool = False,
        value: str = "",
        token: Optional[str] = None,
        help_text: Optional[str] = None,
        input_type: str = "text"
    ) -> None:
        super().__init__(
            name, title=title, aria_label=aria_label, token=token, removable=removable
        )
        self.placeholder = placeholder or ""
        self.value = value
        self.help_text = help_text
        self.input_type = input_type

    def get_template(self) -> str:
        return "pydantic_form/text.jinja2"
