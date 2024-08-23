from pydantic import BaseModel, Field


class Person(BaseModel):
    fistname: str = Field(title="First name")
    lastname: str = Field(title="Last name")
    age: int = Field(title="Age")


class Form(BaseModel):
    person: Person = Field(title="person")
