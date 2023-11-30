from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class Dog(BaseModel):
    nick: str = Field(...)
    breed: Literal["Labrador", "Golden Retriever", "Bulldog"]


class Cat(BaseModel):
    nick: str = Field(...)
    breed: Literal["Persian", "Siamese", "Ragdoll"]


class Person(BaseModel):
    name: str = Field(...)
    pet: Dog | Cat | None = Field(default=None)
    pets: list[Dog | Cat | None] = Field(default_factory=list)

    @field_validator("pets")
    def validate_pets(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value
