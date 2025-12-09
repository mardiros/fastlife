from pydantic import BaseModel, Field, IPvAnyAddress


class Form(BaseModel):
    address: IPvAnyAddress = Field(title="Address")
