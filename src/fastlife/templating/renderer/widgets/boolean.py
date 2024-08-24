from .base import Widget


class BooleanWidget(Widget[bool]):
    def __init__(
        self,
        name: str,
        *,
        title: str | None,
        hint: str | None = None,
        aria_label: str | None = None,
        value: bool = False,
        error: str | None = None,
        removable: bool = False,
        token: str,
    ) -> None:
        super().__init__(
            name,
            title=title,
            hint=hint,
            aria_label=aria_label,
            value=value,
            error=error,
            removable=removable,
            token=token,
        )

    def get_template(self) -> str:
        return "pydantic_form.Boolean"
