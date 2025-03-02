"""Handle EmailStr pydantic type."""

from collections.abc import Mapping
from typing import Any

from pydantic.fields import FieldInfo
from pydantic.networks import EmailStr

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.text import TextWidget
from fastlife.domain.model.types import Builtins


class EmailStrBuilder(BaseWidgetBuilder[Builtins]):
    """Builder for Pydantic EmailStr."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for EmailStr."""
        return issubclass(typ, EmailStr)  # type: ignore

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Builtins | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> TextWidget:
        """Build the widget."""
        return TextWidget(
            name=field_name,
            input_type="email",
            placeholder=str(field.examples[0]) if field and field.examples else None,
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
            autocomplete="email",
        )
