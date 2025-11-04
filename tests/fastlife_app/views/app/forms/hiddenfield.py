from typing import Annotated

from pydantic import BaseModel, Field

from fastlife.adapters.xcomponent.pydantic_form.widgets.base import CustomWidget
from fastlife.adapters.xcomponent.pydantic_form.widgets.hidden import HiddenWidget


class Form(BaseModel):
    id: Annotated[int, CustomWidget(HiddenWidget)] = Field(default=42)
    name: str = Field(title="name")
