from typing import Optional, Sequence, Tuple

from .base import Widget


class DropDownWidget(Widget[str]):
    def __init__(
        self,
        name: str,
        *,
        title: Optional[str],
        hint: Optional[str] = None,
        aria_label: Optional[str] = None,
        value: Optional[str] = None,
        error: str | None = None,
        options: Sequence[Tuple[str, str]] | Sequence[str],
        removable: bool = False,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(
            name,
            value=value,
            error=error,
            title=title,
            token=token,
            removable=removable,
            hint=hint,
            aria_label=aria_label,
        )
        self.options: list[dict[str, str]] = []
        for opt in options:
            if isinstance(opt, tuple):
                self.options.append({"value": opt[0], "text": opt[1]})
            else:
                self.options.append({"value": opt, "text": opt})

    def get_template(self) -> str:
        return "pydantic_form.Dropdown"
