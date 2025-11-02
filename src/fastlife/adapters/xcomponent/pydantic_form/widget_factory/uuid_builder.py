"""Handle simple types (str, int, float, ...)."""

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.base import (
    BaseWidgetBuilder,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.base import Widget
from fastlife.adapters.xcomponent.pydantic_form.widgets.hidden import HiddenWidget


class UuidBuilder(BaseWidgetBuilder[UUID]):
    """Builder for simple types."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for simple types: int, str, float, Decimal, UUID"""
        return issubclass(typ, UUID)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: UUID | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[UUID]:
        """Build the widget."""
        return HiddenWidget(
            name=field_name,
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
