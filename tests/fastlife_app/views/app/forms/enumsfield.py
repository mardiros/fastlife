import enum

from pydantic import BaseModel, Field


class Pet(enum.Enum):
    dog = "lazy dog"
    cat = "crazy cat"
    aligator = "angry aligator"


class Form(BaseModel):
    pets: set[Pet] = Field(title="Pet")
