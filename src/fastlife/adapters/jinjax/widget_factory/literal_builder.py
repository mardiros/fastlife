"""Handle Literal type."""

from collections.abc import Mapping
from typing import Any, Literal

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.dropdown import DropDownWidget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget
from fastlife.domain.model.types import AnyLiteral


class LiteralBuilder(BaseWidgetBuilder[AnyLiteral]):
    """Builder for Literal."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for Literal."""
        return origin is Literal

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],  # a literal actually
        field: FieldInfo | None,
        value: AnyLiteral | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> HiddenWidget | DropDownWidget:
        """Build the widget."""
        choices: list[str] = field_type.__args__  # type: ignore
        if len(choices) == 1:
            return HiddenWidget(
                name=field_name,
                value=choices[0],
                token=self.factory.token,
            )
        return DropDownWidget(
            name=field_name,
            options=choices,  # type: ignore
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
        )
