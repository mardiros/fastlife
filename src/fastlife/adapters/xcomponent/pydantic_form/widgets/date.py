from datetime import date, datetime

from pydantic import Field

from .base import Widget


class DateWidget(Widget[date]):
    """
    Widget for text like field (email, ...).
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{globals.gettext(title)}</Label>
        <OptionalErrorText text={error} />
        <Date name={name} value={value} type={input_type} id={id}
          aria-label={aria_label} min={min} max={max} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    input_type: str = Field(default="date")
    """type attribute for the Input component."""
    min: date | None = Field(default=None)
    max: date | None = Field(default=None)


class DateTimeWidget(Widget[datetime]):
    """
    Widget for text like field (email, ...).
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <Label for={id}>{globals.gettext(title)}</Label>
        <OptionalErrorText text={error} />
        <DateTime name={name} value={value} type={input_type} id={id}
          aria-label={aria_label} min={min} max={max} />
        <Hint text={hint} />
      </div>
    </Widget>
    """

    input_type: str = Field(default="datetime-local")
    """type attribute for the Input component."""
    min: date | None = Field(default=None)
    max: date | None = Field(default=None)
