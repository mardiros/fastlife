"""Handle Pydantic SecretStr type."""

from collections.abc import Mapping
from typing import Any

from pydantic import SecretStr
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.text import PasswordWidget


class SecretStrBuilder(BaseWidgetBuilder[SecretStr]):
    """Builder for Pydantic SecretStr."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for Pydantic SecretStr."""
        return issubclass(typ, SecretStr)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: SecretStr | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[SecretStr]:
        """Build the widget."""
        return PasswordWidget(
            name=field_name,
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
            error=form_errors.get(field_name),
            new_password="new-password" in field.metadata if field else False,
        )
