from datetime import date

from pydantic import BaseModel, Field


class Form(BaseModel):
    rdv: date = Field(title="rendez-vous")
