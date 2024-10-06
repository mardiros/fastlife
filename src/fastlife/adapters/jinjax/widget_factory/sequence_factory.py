"""
Mixin for sequence and set.
"""

from collections.abc import Callable, Mapping, Sequence
from enum import Enum
from typing import Any, Literal, get_origin

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.checklist import Checkable, ChecklistWidget
from fastlife.adapters.jinjax.widgets.sequence import SequenceWidget


class SequenceFactoryMixin:
    token: str
    build: Callable[..., Any]

    def build_sequence(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Sequence[Any] | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        typ = field_type.__args__[0]  # type: ignore
        value = value or []
        items = [
            self.build(
                typ,  # type: ignore
                name=f"{field_name}.{idx}",
                value=v,
                field=field,
                form_errors=form_errors,
                removable=True,
            )
            for idx, v in enumerate(value)
        ]
        return SequenceWidget(
            field_name,
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            value=items,
            item_type=typ,  # type: ignore
            token=self.token,
            removable=removable,
            error=form_errors.get(field_name),
        )

    def build_set(
        self,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Sequence[Any] | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
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
                        token=self.token,
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
                    token=self.token,
                    error=form_errors.get(f"{field_name}-{e.name}"),
                )
                for e in choice_wrapper
            ]
        else:
            raise NotImplementedError  # coverage: ignore

        return ChecklistWidget(
            field_name,
            title=field.title if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.token,
            value=choices,
            removable=removable,
            error=form_errors.get(field_name),
        )
