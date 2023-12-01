from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class Dog(BaseModel):
    nick: str = Field(title="Nick name", description="Say it, he will wag its tail")
    breed: Literal["Labrador", "Golden Retriever", "Bulldog"]


class Cat(BaseModel):
    nick: str = Field(title="Nick name", description="Say it, nothing will happen")
    breed: Literal["Persian", "Siamese", "Ragdoll"]


class Person(BaseModel):
    name: str = Field(
        title="name",
        description="First name and last name, or surname",
        examples=["John doe"],
    )
    pet: Dog | Cat | None = Field(default=None)
    pets: list[Dog | Cat | None] = Field(default_factory=list, title="pets")

    @field_validator("pets")
    def validate_pets(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value
