from typing import Any

from .base import Widget


class HiddenWidget(Widget[str]):
    '''
    Widget to annotate to display a field as an hidden field.

    ::
        from pydantic import BaseModel
        from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget

        class MyForm(BaseModel):
            id: Annotated[str, HiddenWidget] = Field(...)
            """Identifier in the database."""

    '''

    def __init__(
        self,
        name: str,
        *,
        value: str,
        token: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, value=value, token=token)

    def get_template(self) -> str:
        return "pydantic_form.Hidden.jinja"
