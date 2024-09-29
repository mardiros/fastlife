import enum

from pydantic import BaseModel, Field


class Gender(enum.Enum):
    male = "male"
    female = "female"


class Form(BaseModel):
    gender: Gender = Field(title="Gender")
