from typing import Optional

from .base import Widget


class TextWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        placeholder: Optional[str] = None,
        required: bool = False,
        value: str = "",
        id: Optional[str] = None,
        help_text: Optional[str] = None,
    ) -> None:
        super().__init__(name, title, id, required=required)
        self.placeholder = placeholder or ""
        self.value = value
        self.help_text = help_text

    def get_template(self) -> str:
        return "pydantic_form/text.jinja2"
