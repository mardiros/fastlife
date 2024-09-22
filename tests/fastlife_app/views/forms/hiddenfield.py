from typing import Annotated

from pydantic import BaseModel, Field

from fastlife.templates.renderer.widgets.hidden import HiddenWidget


class Form(BaseModel):
    id: Annotated[int, HiddenWidget] = Field(default=42)
    name: str = Field(title="name")
