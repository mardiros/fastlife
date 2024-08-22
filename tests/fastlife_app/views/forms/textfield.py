from pydantic import BaseModel, Field


class Form(BaseModel):
    nick: str = Field(title="nickname")
