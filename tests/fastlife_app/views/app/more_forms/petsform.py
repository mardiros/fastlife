from typing import Annotated
from uuid import UUID, uuid1

from pydantic import BaseModel, Field

from fastlife.adapters.jinjax.widgets.base import CustomWidget, Widget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget
from fastlife.adapters.jinjax.widgets.text import TextareaWidget


class MyWidget(Widget[str]):
    def get_template(self) -> str:
        return "MyWidget.jinja"


class PetForm(BaseModel):
    id: Annotated[UUID, CustomWidget(HiddenWidget)] = Field(default_factory=uuid1)
    nick: Annotated[str, CustomWidget(MyWidget)] = Field(title="Pet's Name")
    description: Annotated[str, CustomWidget(TextareaWidget)] = Field(
        title="Pet's hobbies"
    )
    favorite_toy: str = Field(title="Favorite Toy")
    magic_power: bool = Field(title="Has Magic Power")
