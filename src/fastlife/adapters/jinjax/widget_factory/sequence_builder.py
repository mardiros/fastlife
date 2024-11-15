"""Handle Sequence type."""

from collections.abc import Mapping, MutableSequence, Sequence
from typing import Any

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.sequence import SequenceWidget


class SequenceBuilder(BaseWidgetBuilder[Sequence[Any]]):
    """Builder for Sequence values."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for Sequence, MutableSequence or list"""
        return origin is Sequence or origin is MutableSequence or origin is list

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Sequence[Any] | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Sequence[Any]]:
        """Build the widget."""
        typ = field_type.__args__[0]  # type: ignore
        value = value or []
        items: Sequence[Any] = [
            self.factory.build(
                typ,  # type: ignore
                name=f"{field_name}.{idx}",
                value=v,
                field=field,
                form_errors=form_errors,
                removable=True,
            )
            for idx, v in enumerate(value)
        ]
        return SequenceWidget[Any](
            name=field_name,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            value=items,
            item_type=typ,  # type: ignore
            token=self.factory.token,
            removable=removable,
            error=form_errors.get(field_name),
        )
