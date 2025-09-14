"""
Widget for field of type Enum or Literal.
"""

from collections.abc import Sequence

from pydantic import Field, field_validator
from typing_extensions import TypedDict

from fastlife.adapters.xcomponent.catalog import catalog

from .base import Widget

OptionItem = str | int


class Option(TypedDict):
    value: OptionItem
    text: OptionItem


@catalog.component
def DropDownWidgetOption(id: str, opt: Option) -> str:
    return """
    <Option
        value={opt.value}
        id={id + "-" + opt.value.replace(" ", " -")}
        selected={value and value == opt.value}
        >
      {globals.gettext(opt.text)}
    </Option>
    """


class DropDownWidget(Widget[str]):
    """
    Widget for field of type Enum or Literal.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{ globals.gettext(title) }</Label>
        <Select name={name} id={id}>
          {
            for opt in options  {
              <DropDownWidgetOption id={id} opt={opt} value={value}/>
            }
          }
        </Select>
        <OptionalErrorText text={error} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    options: list[Option] = Field(default_factory=list)

    @field_validator("options", mode="before")
    @classmethod
    def validate_options(
        cls, options: Sequence[OptionItem | tuple[OptionItem, OptionItem]] | None
    ) -> Sequence[Option]:
        if not options:
            return []
        ret: list[Option] = []
        for opt in options:
            if isinstance(opt, tuple):
                ret.append({"value": opt[0], "text": opt[1]})
            else:
                ret.append({"value": opt, "text": opt})
        return ret
