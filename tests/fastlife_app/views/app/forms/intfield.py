from typing import Any

from pydantic import BaseModel, Field, field_validator


class Form(BaseModel):
    seconds: int | None = Field(title="seconds")

    @field_validator("seconds", mode="before")
    def validat_seconds(cls, value: Any) -> Any:
        return None if value == "" else value
