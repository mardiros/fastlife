"""
Widget for field of type Enum or Literal.
"""

from collections.abc import Sequence

from pydantic import Field, field_validator

from .base import Widget


class DropDownWidget(Widget[str]):
    """
    Widget for field of type Enum or Literal.
    """

    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <Label :for="id">{{title}}</Label>
        <Select :name="name" :id="id">
          {%- for opt in options -%}
          <Option :value="opt.value" id={{id + "-" + opt.value.replace(" ", " -")}}
            :selected="value==opt.value">
            {{- opt.text -}}
          </Option>
          {%- endfor -%}
        </Select>
        <pydantic_form.Error :text="error" />
        <pydantic_form.Hint :text="hint" />
      </div>
    </pydantic_form.Widget>
    """

    options: list[dict[str | int, str | int]] = Field(default_factory=list)

    @field_validator("options", mode="before")
    @classmethod
    def validate_options(
        cls, options: Sequence[str | int | tuple[str | int, str | int]] | None
    ) -> Sequence[dict[str | int, str | int]]:
        if not options:
            return []
        ret: list[dict[str | int, str | int]] = []
        for opt in options:
            if isinstance(opt, tuple):
                ret.append({"value": opt[0], "text": opt[1]})
            else:
                ret.append({"value": opt, "text": opt})
        return ret
