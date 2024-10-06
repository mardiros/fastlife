"""Build for enum and literals."""

from collections.abc import Callable, Mapping
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.dropdown import DropDownWidget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget


class EnumFactoryMixin:
    token: str
    build: Callable[..., Any]

    def build_literal(
        self,
        field_name: str,
        field_type: type[Any],  # a literal actually
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        choices: list[str] = field_type.__args__  # type: ignore
        if len(choices) == 1:
            return HiddenWidget(
                field_name,
                value=choices[0],
                token=self.token,
            )
        return DropDownWidget(
            field_name,
            options=choices,
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

    def build_enum(
        self,
        field_name: str,
        field_type: type[Any],  # an enum subclass
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        options = [(item.name, item.value) for item in field_type]  # type: ignore
        return DropDownWidget(
            field_name,
            options=options,  # type: ignore
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
