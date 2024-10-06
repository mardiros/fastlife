"""
Mixin for model.
"""

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.model import ModelWidget


class ModelFactoryMixin:
    token: str
    build: Callable[..., Any]

    def build_model(
        self,
        field_name: str,
        typ: type[BaseModel],
        field: FieldInfo | None,
        value: Mapping[str, Any],
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        ret: dict[str, Any] = {}
        for key, child_field in typ.model_fields.items():
            child_key = f"{field_name}.{key}" if field_name else key
            if child_field.exclude:
                continue
            if child_field.annotation is None:
                raise ValueError(  # coverage: ignore
                    f"Missing annotation for {child_field} in {child_key}"
                )
            ret[key] = self.build(
                child_field.annotation,
                name=child_key,
                field=child_field,
                value=value.get(key),
                form_errors=form_errors,
                removable=False,
            )
        return ModelWidget(
            field_name,
            value=list(ret.values()),
            removable=removable,
            title=field.title if field and field.title else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            error=form_errors.get(field_name),
            nested=field is not None,
        )
