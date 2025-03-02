from pydantic import Field

from .base import Widget


class MFACodeWidget(Widget[str]):
    """
    Widget for MFA code such as TOTP token.
    """

    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <Label :for="id">{{title}}</Label>
        <pydantic_form.Error :text="error" />
        <Input :name="name" type="text" :id="id" inputmode="numeric"
            autocomplete="one-time-code" :autofocus="autofocus"
          :aria-label="aria_label" :placeholder="placeholder" />
        <pydantic_form.Hint :text="hint" />
      </div>
    </pydantic_form.Widget>
    """

    placeholder: str | None = Field(default=None)
    autofocus: bool = Field(default=True)
