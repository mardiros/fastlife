import enum
from typing import Set
from pydantic import BaseModel, Field


class Pet(enum.Enum):
    dog = "lazy dog"
    cat = "crazy cat"
    aligator = "angry aligator"


class Form(BaseModel):
    pets: Set[Pet] = Field(title="Pet")
