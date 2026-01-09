"""Handle boolean values."""

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.base import (
    BaseWidgetBuilder,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.date import (
    DateTimeWidget,
    DateWidget,
)


class DateBuilder(BaseWidgetBuilder[date]):
    """Builder for date."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for date."""
        return issubclass(typ, date)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: date | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> DateWidget:
        """Build the widget."""
        return DateWidget(
            name=field_name,
            removable=removable,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            value=value,
            error=form_errors.get(field_name),
            # FIXME convert annoation to have min and max here
        )


class DateTimeBuilder(BaseWidgetBuilder[date]):
    """Builder for datetime."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for date."""
        return issubclass(typ, datetime)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: date | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> DateTimeWidget:
        """Build the widget."""
        return DateTimeWidget(
            name=field_name,
            removable=removable,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            value=value,
            error=form_errors.get(field_name),
            # FIXME convert annoation to have min and max here
        )
