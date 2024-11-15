"""Handle Enum type."""

from collections.abc import Mapping
from enum import Enum
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.dropdown import DropDownWidget


class EnumBuilder(BaseWidgetBuilder[Enum]):
    """Builder for Enum."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for Enum."""
        return issubclass(typ, Enum)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],  # an enum subclass
        field: FieldInfo | None,
        value: Enum | None,  # str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Enum]:
        """Build the widget."""
        options = [(item.name, item.value) for item in field_type]  # type: ignore
        return DropDownWidget(
            name=field_name,
            options=options,  # type: ignore
            removable=removable,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            value=str(value),
            error=form_errors.get(field_name),
        )
