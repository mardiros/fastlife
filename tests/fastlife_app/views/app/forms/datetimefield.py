from datetime import datetime

from pydantic import BaseModel, Field


class Form(BaseModel):
    rdv: datetime = Field(title="rendez-vous")
