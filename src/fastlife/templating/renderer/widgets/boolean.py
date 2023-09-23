from typing import Optional
from .base import Widget


class BooleanWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        value: bool = False,
        id: Optional[str] = None,
    ) -> None:
        super().__init__(name, title, id)
        self.value = value
        self.id = id or name  # fixme

    def get_template(self) -> str:
        return "pydantic_form/boolean.jinja2"
