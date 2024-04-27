from typing import Sequence

from pydantic import BaseModel, Field

from .base import Widget


class Checkable(BaseModel):
    label: str
    name: str
    value: str
    token: str
    checked: bool
    error: str | None = Field(default=None)

    @property
    def id(self) -> str:
        id = f"{self.name}-{self.value}-{self.token}"
        return id.replace(".", "-").replace("_", "-")

    @property
    def field_name(self) -> str:
        return f"{self.name}[]"


class ChecklistWidget(Widget[Sequence[Checkable]]):
    def __init__(
        self,
        name: str,
        *,
        title: str | None,
        value: Sequence[Checkable],
        error: str | None = None,
        token: str,
        removable: bool,
    ) -> None:
        super().__init__(
            name,
            value=value,
            error=error,
            token=token,
            title=title,
            removable=removable,
        )

    def get_template(self) -> str:
        return "pydantic_form.Checklist"
