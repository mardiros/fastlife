"""Handle Set type."""

from collections.abc import Mapping
from enum import Enum
from typing import Any, Literal, get_origin

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widget_factory.base import BaseWidgetBuilder
from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.checklist import Checkable, ChecklistWidget


class SetBuilder(BaseWidgetBuilder[set[Any]]):
    """Builder for Set."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for Set"""
        return origin is set

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: set[Any] | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        """Build the widget."""
        choice_wrapper = field_type.__args__[0]
        choices = []
        choice_wrapper_origin = get_origin(choice_wrapper)
        if choice_wrapper_origin:
            if choice_wrapper_origin is Literal:
                litchoice: list[str] = choice_wrapper.__args__  # type: ignore
                choices = [
                    Checkable(
                        label=c,
                        value=c,
                        checked=c in value if value else False,  # type: ignore
                        name=field_name,
                        token=self.factory.token,
                        error=form_errors.get(f"{field_name}-{c}"),
                    )
                    for c in litchoice
                ]

            else:
                raise NotImplementedError  # coverage: ignore
        elif issubclass(choice_wrapper, Enum):
            choices = [
                Checkable(
                    label=e.value,
                    value=e.name,
                    checked=e.name in value if value else False,  # type: ignore
                    name=field_name,
                    token=self.factory.token,
                    error=form_errors.get(f"{field_name}-{e.name}"),
                )
                for e in choice_wrapper
            ]
        else:
            raise NotImplementedError  # coverage: ignore

        return ChecklistWidget(
            name=field_name,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            value=choices,
            removable=removable,
            error=form_errors.get(field_name),
        )
