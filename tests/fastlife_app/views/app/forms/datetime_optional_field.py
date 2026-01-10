from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Form(BaseModel):
    rdv: datetime | None = Field(title="rendez-vous")

    @field_validator("rdv", mode="before")
    @classmethod
    def filter_empty_string(cls, value: Any) -> Any:
        if not value:
            return None
        return value
