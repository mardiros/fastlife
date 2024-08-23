from typing import Literal, Set
from pydantic import BaseModel, Field


Hobby = Literal['cooking', 'reading', 'smoking']

class Form(BaseModel):
    hobbies: Set[Hobby] = Field(title="Hobbies")
