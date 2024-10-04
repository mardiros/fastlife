from typing import Literal

from pydantic import BaseModel


class Dog(BaseModel):
    type: Literal["dog"]
    nick: str


class Cat(BaseModel):
    type: Literal["cat"]
    nick: str


class Form(BaseModel):
    pet: Dog | Cat
