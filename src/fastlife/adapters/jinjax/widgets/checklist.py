"""
Widget for field of type Set.
"""

from collections.abc import Sequence
from typing import Self

from pydantic import BaseModel, Field, model_validator

from .base import Widget


class Checkable(BaseModel):
    """A checkable field from a checklist."""

    label: str
    name: str
    value: str
    token: str
    checked: bool
    error: str | None = Field(default=None)

    id: str | None = Field(default=None)
    field_name: str | None = Field(default=None)

    @model_validator(mode="after")
    def fill_props(self) -> Self:
        self.id = f"{self.name}-{self.value}-{self.token}".replace(".", "-")
        self.field_name = f"{self.name}[]"
        return self


class ChecklistWidget(Widget[Sequence[Checkable]]):
    """
    Widget for field of type Set.
    """

    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <Details>
          <Summary :id="id + '-summary'">
            <H3 :class="H3_SUMMARY_CLASS">{{title}}</H3>
            <pydantic_form.Error :text="error" />
          </Summary>
          <div>
            {% for value in value %}
            <div class="flex items-center mb-4">
                <Checkbox :name="value.field_name" type="checkbox"
                    :id="value.id"
                    :value="value.value"
                    :checked="value.checked" />
                <Label :for="value.id"
                    class="ms-2 text-base text-neutral-900 dark:text-white">
                    {{- value.label -}}
                </Label>
                <pydantic_form.Error :text="value.error" />
            </div>
            {% endfor %}
          </div>
        </Details>
      </div>
    </pydantic_form.Widget>
    """
