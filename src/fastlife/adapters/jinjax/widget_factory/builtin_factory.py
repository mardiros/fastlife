"""Add factory for builtin types and simple types added by pydantic such as secrets."""

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import SecretStr
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.boolean import BooleanWidget
from fastlife.adapters.jinjax.widgets.text import TextWidget


class BuiltinFactoryMixin:
    token: str
    build: Callable[..., Any]

    def build_boolean(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: bool,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return BooleanWidget(
            field_name,
            removable=removable,
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            value=value,
            error=form_errors.get(field_name),
        )

    def build_emailtype(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return TextWidget(
            field_name,
            input_type="email",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )

    def build_secretstr(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: SecretStr | str,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return TextWidget(
            field_name,
            input_type="password",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            value=value.get_secret_value() if isinstance(value, SecretStr) else value,
            error=form_errors.get(field_name),
        )

    def build_simpletype(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
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
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )
