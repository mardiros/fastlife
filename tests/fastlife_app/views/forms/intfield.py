from pydantic import BaseModel, Field


class Form(BaseModel):
    seconds: int = Field(title="seconds")
