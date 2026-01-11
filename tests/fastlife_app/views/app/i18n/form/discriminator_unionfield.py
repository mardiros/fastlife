from typing import Annotated, Literal

from pydantic import BaseModel, Field

from tests.fastlife_app.views.app.i18n.dummy_messages import gettext


class Dog(BaseModel):
    type: Literal["dog"]
    nick: str
    meows: int


class Cat(BaseModel):
    type: Literal["cat"]
    nick: str
    barks: float


class Form(BaseModel):
    pet: Annotated[Dog, gettext("The Dog")] | Annotated[Cat, gettext("The Cat")] = (
        Field(discriminator="type")
    )
