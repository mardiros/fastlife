from typing import Optional, Sequence, Tuple

from .base import Widget


class DropDownWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        options: Sequence[Tuple[str, str]] | Sequence[str],
        removable: bool = False,
        value: str = "",
        token: Optional[str] = None,
        help_text: Optional[str] = None,
    ) -> None:
        super().__init__(name, title=title, token=token, removable=removable)
        self.options: list[dict[str, str]] = []
        for opt in options:
            if isinstance(opt, tuple):
                self.options.append({"value": opt[0], "text": opt[1]})
            else:
                self.options.append({"value": opt, "text": opt})
        self.value = value
        self.help_text = help_text

    def get_template(self) -> str:
        return "pydantic_form.Dropdown"
