from collections.abc import Sequence
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator

from fastlife.adapters.jinjax.widgets.text import TextareaWidget


class Form(BaseModel):
    aliases: Annotated[Sequence[str], TextareaWidget] = Field(
        title="Aliases", description="One alias per line", default_factory=list
    )

    @field_validator("aliases", mode="before")
    def split(cls, s: Any) -> Sequence[str]:
        return s.split() if s else []
