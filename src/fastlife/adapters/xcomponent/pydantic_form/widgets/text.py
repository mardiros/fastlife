from collections.abc import Sequence
from typing import Any

from pydantic import Field, SecretStr

from fastlife.adapters.xcomponent.catalog import catalog
from fastlife.domain.model.types import Builtins

from .base import Widget


@catalog.function
def is_str(value: Any) -> bool:
    return isinstance(value, str)


class TextWidget(Widget[Builtins]):
    """
    Widget for text like field (email, ...).
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{globals.gettext(title)}</Label>
        <OptionalErrorText text={error} />
        <Input name={name} value={value} type={input_type} id={id}
          aria-label={aria_label} placeholder={placeholder}
         autocomplete={autocomplete} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    input_type: str = Field(default="text")
    """type attribute for the Input component."""
    placeholder: str | None = Field(default=None)
    """placeholder attribute for the Input component."""
    autocomplete: str | None = Field(default=None)
    """autocomplete attribute for the Input component."""


class PasswordWidget(Widget[SecretStr]):
    """
    Widget for password fields.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{globals.gettext(title)}</Label>
        <OptionalErrorText text={error} />
        <Password name={name} type={input_type} id={id}
          autocomplete={
            if new_password {
              <>new-password</>
            }
            else {
              <>current-password</>
            }
          }
          aria-label={aria_label} placeholder={placeholder} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    input_type: str = Field(default="password")
    """type attribute for the Input component."""
    placeholder: str | None = Field(default=None)
    """placeholder attribute for the Input component."""
    new_password: bool = Field(default=False)
    """
    Adapt autocomplete behavior for browsers to hint existing or generate password.
    """


class TextareaWidget(Widget[str | Sequence[str]]):
    """
    Render a Textearea for a string or event a sequence of string.

    ```
    from fastlife.adapters.jinjax.widgets.base import CustomWidget
    from fastlife.adapters.jinjax.widgets.text import TextareaWidget
    from pydantic import BaseModel, Field, field_validator

    class TaggedParagraphForm(BaseModel):
        paragraph: Annotated[str, CustomWidget(TextareaWidget)] = Field(...)
        tags: Annotated[Sequence[str], CustomWidget(TextareaWidget)] = Field(
            default_factory=list,
            title="Tags",
            description="One tag per line",
        )

        @field_validator("tags", mode="before")
        def split(cls, s: Any) -> Sequence[str]:
            return s.split() if s else []
    ```
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{globals.gettext(title)}</Label>
        <OptionalErrorText text={error} />
        <Textarea name={name} id={id} aria-label={aria_label}>
            {
              if is_str(value) {
                value
              }
              else {
                for v in value {
                  v + "\n"
                }
              }
            }
        </Textarea>
        <Hint text={hint} />
      </div>
    </Widget>
    """
