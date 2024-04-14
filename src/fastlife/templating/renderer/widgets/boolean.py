from typing import Optional

from .base import Widget


class BooleanWidget(Widget[bool]):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        value: bool = False,
        removable: bool = False,
        token: str,
    ) -> None:
        super().__init__(
            name, title=title, value=value, removable=removable, token=token
        )

    def get_template(self) -> str:
        return "pydantic_form.Boolean"
