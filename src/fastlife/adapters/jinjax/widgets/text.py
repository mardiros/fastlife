from collections.abc import Sequence

from pydantic import Field

from fastlife.domain.model.types import Builtins

from .base import Widget


class TextWidget(Widget[Builtins]):
    """
    Widget for text like field (email, ...).
    """

    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <Label :for="id">{{title}}</Label>
        <pydantic_form.Error :text="error" />
        <Input :name="name" :value="value" :type="input_type" :id="id"
          :aria-label="aria_label" :placeholder="placeholder" />
        <pydantic_form.Hint :text="hint" />
      </div>
    </pydantic_form.Widget>
    """

    input_type: str = Field(default="text")
    placeholder: str | None = Field(default=None)


class TextareaWidget(Widget[Sequence[str]]):
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
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <Label :for="id">{{title}}</Label>
        <pydantic_form.Error :text="error" />
        <Textarea :name="name" :id="id" :aria-label="aria_label">
            {%- if v is string -%}
            {{- v -}}}
            {%- else -%}
            {%- for v in value %}{{v}}
    {% endfor -%}
            {% endif %}
        </Textarea>
        <pydantic_form.Hint :text="hint" />
      </div>
    </pydantic_form.Widget>
    """

    placeholder: str = Field(default="")
