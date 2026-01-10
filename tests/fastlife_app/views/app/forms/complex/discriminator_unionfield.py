from typing import Literal

from pydantic import BaseModel, Field


class Dog(BaseModel):
    type: Literal["dog"]
    nick: str
    meows: int


class Cat(BaseModel):
    type: Literal["cat"]
    nick: str
    barks: float


class Form(BaseModel):
    pet: Dog | Cat = Field(discriminator="type")
