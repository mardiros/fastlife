from pydantic import Field

from .base import Widget


class MFACodeWidget(Widget[str]):
    """
    Widget for MFA code such as TOTP token.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{ globals.gettext(title) }</Label>
        <OptionalErrorText text={error} />
        <Input name={name} id={id} inputmode="numeric"
            autocomplete="one-time-code" autofocus={autofocus}
            aria-label={aria_label} placeholder={placeholder} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    placeholder: str | None = Field(default=None)
    autofocus: bool = Field(default=True)
