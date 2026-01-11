from typing import Literal

from pydantic import BaseModel, Field


class Dog(BaseModel):
    type: Literal["dog"]
    nick: str


class Cat(BaseModel):
    type: Literal["cat"]
    nick: str


class Form(BaseModel):
    pet: Dog | Cat = Field(discriminator="type")
