"""
Create markup for pydantic forms.
"""

from collections.abc import Callable, Mapping
from types import NoneType
from typing import Any

from pydantic import ValidationError
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.union import UnionWidget
from fastlife.shared_utils.infer import is_complex_type


class UnionFactoryMixin:
    token: str
    build: Callable[..., Any]

    def build_union(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Any,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        types: list[type[Any]] = []
        # required = True
        for typ in field_type.__args__:  # type: ignore
            if typ is NoneType:
                # required = False
                continue
            types.append(typ)  # type: ignore

        if (
            not removable
            and len(types) == 1
            # if the optional type is a complex type,
            and not is_complex_type(types[0])
        ):
            return self.build(
                types[0],
                name=field_name,
                field=field,
                value=value,
                form_errors=form_errors,
                removable=False,
            )
        child = None
        if value:
            for typ in types:
                try:
                    typ(**value)
                except ValidationError:
                    pass
                else:
                    child = self.build(
                        typ,
                        name=field_name,
                        field=field,
                        value=value,
                        form_errors=form_errors,
                        removable=False,
                    )

        widget = UnionWidget(
            field_name,
            # we assume those types are BaseModel
            value=child,
            children_types=types,  # type: ignore
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            removable=removable,
            error=form_errors.get(field_name),
        )

        return widget
