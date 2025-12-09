from pydantic import Field, IPvAnyAddress

from .base import Widget


class IpAddressWidget(Widget[IPvAnyAddress]):
    """
    Widget for Ip Address.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{ globals.gettext(title) }</Label>
        <OptionalErrorText text={error} />
        <Input name={name} id={id}
            value={str(value)}
            type="text"
            pattern="^((\\d{1,3}\\.){3}\\d{1,3})|([0-9a-fA-F:]+)$"
            autocomplete={autocomplete}
            aria-label={aria_label} placeholder={placeholder} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    placeholder: str | None = Field(default=None)
    autocomplete: str | None = Field(default=None)
    """autocomplete attribute for the Input component."""
