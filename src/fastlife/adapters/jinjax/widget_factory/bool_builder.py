"""Handle boolean values."""

from collections.abc import Mapping
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.boolean import BooleanWidget


class BoolBuilder(BaseWidgetBuilder[bool]):
    """Builder for boolean."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for boolean."""
        return issubclass(typ, bool)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: bool | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> BooleanWidget:
        """Build the widget."""
        return BooleanWidget(
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
            value=value or False,
            error=form_errors.get(field_name),
        )
