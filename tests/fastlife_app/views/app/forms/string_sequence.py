from typing import Sequence

from pydantic import BaseModel, Field


class Form(BaseModel):
    aliases: Sequence[str] = Field(title="Aliases")
