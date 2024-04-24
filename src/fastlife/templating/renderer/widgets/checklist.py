from typing import Sequence

from pydantic import BaseModel
from .base import Widget


class Checkable(BaseModel):
    label: str
    name: str
    value: str
    token: str
    checked: bool

    @property
    def id(self):
        id = f"{self.name}-{self.value}-{self.token}"
        return id.replace(".", "-").replace("_", "-")


class ChecklistWidget(Widget[Sequence[Checkable]]):
    def __init__(
        self,
        name: str,
        *,
        title: str | None,
        value: Sequence[Checkable],
        token: str,
    ) -> None:
        super().__init__(name, value=value, token=token)
        self.title = title or ""

    def get_template(self) -> str:
        return "pydantic_form.Checklist"
