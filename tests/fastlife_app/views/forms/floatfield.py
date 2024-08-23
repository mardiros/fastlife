from pydantic import BaseModel, Field


class Form(BaseModel):
    fm: float = Field(title="fm station")
