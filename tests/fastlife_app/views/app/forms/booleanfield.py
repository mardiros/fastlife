from pydantic import BaseModel, Field


class Form(BaseModel):
    aggreed: bool = Field(title="Accept contract")
