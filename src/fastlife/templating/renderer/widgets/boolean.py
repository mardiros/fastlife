from typing import Optional

from .base import Widget


class BooleanWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        value: bool = False,
        required: bool = False,
        token: str,
    ) -> None:
        super().__init__(name, title=title, required=required, token=token)
        self.value = value

    def get_template(self) -> str:
        return "pydantic_form/boolean.jinja2"
