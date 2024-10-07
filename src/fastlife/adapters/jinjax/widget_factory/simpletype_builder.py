"""Add factory for builtin types and simple types added by pydantic such as secrets."""

from collections.abc import Mapping
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.text import TextWidget


class SimpleTypeBuilder(BaseWidgetBuilder[str | int | str | float | Decimal | UUID]):
    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        return issubclass(typ, int | str | float | Decimal | UUID)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: int | str | float | Decimal | UUID | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[int | str | float | Decimal | UUID]:
        return TextWidget(
            field_name,
            placeholder=str(field.examples[0]) if field and field.examples else None,
            title=field.title if field else "",
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
