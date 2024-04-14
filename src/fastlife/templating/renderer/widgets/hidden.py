from .base import Widget


class HiddenWidget(Widget[str]):
    def __init__(
        self,
        name: str,
        *,
        value: str,
        token: str,
    ) -> None:
        super().__init__(name, value=value, token=token)

    def get_template(self) -> str:
        return "pydantic_form.Hidden"
