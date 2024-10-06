from typing import Annotated
from uuid import UUID, uuid1

from pydantic import BaseModel, Field

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget
from fastlife.adapters.jinjax.widgets.text import TextareaWidget


class MyWidget(Widget[str]):
    def get_template(self) -> str:
        return "MyWidget.jinja"


class PetForm(BaseModel):
    id: Annotated[UUID, HiddenWidget] = Field(default=uuid1)
    nick: Annotated[str, MyWidget] = Field(title="Pet's Name")
    description: Annotated[str, TextareaWidget] = Field(title="Pet's hobbies")
    favorite_toy: str = Field(title="Favorite Toy")
    magic_power: bool = Field(title="Has Magic Power")
