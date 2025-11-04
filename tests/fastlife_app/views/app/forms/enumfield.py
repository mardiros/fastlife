import enum

from pydantic import BaseModel, Field


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Form(BaseModel):
    gender: Gender = Field(title="Gender")
