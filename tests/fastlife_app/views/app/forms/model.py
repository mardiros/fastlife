from pydantic import BaseModel, Field


class Person(BaseModel):
    firstname: str = Field(title="First name")
    lastname: str = Field(title="Last name")
    age: int = Field(title="Age")


class Form(BaseModel):
    professor: Person = Field(title="Knowledge Guru")
