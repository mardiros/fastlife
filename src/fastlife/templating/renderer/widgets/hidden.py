from .base import Widget


class HiddenWidget(Widget):
    def __init__(
        self,
        name: str,
        *,
        value: str,
        token: str,
    ) -> None:
        super().__init__(name, token=token)
        self.value = value

    def get_template(self) -> str:
        return "pydantic_form/hidden.jinja2"
