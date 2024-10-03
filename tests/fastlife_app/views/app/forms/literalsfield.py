from typing import Literal

from pydantic import BaseModel, Field

Hobby = Literal["cooking", "reading", "smoking"]


class Form(BaseModel):
    hobbies: set[Hobby] = Field(title="Hobbies")
