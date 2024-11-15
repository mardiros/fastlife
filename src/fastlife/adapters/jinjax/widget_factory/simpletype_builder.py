"""Handle simple types (str, int, float, ...)."""

from collections.abc import Mapping
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.text import TextWidget
from fastlife.domain.model.types import Builtins


class SimpleTypeBuilder(BaseWidgetBuilder[Builtins]):
    """Builder for simple types."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for simple types: int, str, float, Decimal, UUID"""
        return issubclass(typ, Builtins)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Builtins | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Builtins]:
        """Build the widget."""
        return TextWidget(
            name=field_name,
            placeholder=str(field.examples[0]) if field and field.examples else None,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            removable=removable,
            token=self.factory.token,
            value=str(value) if value else "",
            error=form_errors.get(field_name),
        )
