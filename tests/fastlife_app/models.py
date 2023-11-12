from typing import Literal

from pydantic import BaseModel, Field


class Dog(BaseModel):
    nick: str = Field(...)
    breed: Literal["Labrador", "Golden Retriever", "Bulldog"]


class Cat(BaseModel):
    nick: str = Field(...)
    breed: Literal["Persian", "Siamese", "Ragdoll"]


class Person(BaseModel):
    name: str = Field(...)
    pet: Dog | Cat | None = Field(default=None)
