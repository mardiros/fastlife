import secrets
from collections.abc import MutableSequence, Sequence
from decimal import Decimal
from enum import Enum
from inspect import isclass
from types import NoneType
from typing import Any, Literal, Mapping, Optional, Type, cast, get_origin
from uuid import UUID

from markupsafe import Markup
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from pydantic.fields import FieldInfo

from fastlife.request.model_result import ModelResult
from fastlife.shared_utils.infer import is_complex_type, is_union
from fastlife.templating.renderer.abstract import AbstractTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
from fastlife.templating.renderer.widgets.checklist import Checkable, ChecklistWidget
from fastlife.templating.renderer.widgets.dropdown import DropDownWidget
from fastlife.templating.renderer.widgets.hidden import HiddenWidget
from fastlife.templating.renderer.widgets.sequence import SequenceWidget

from .base import Widget, get_title
from .model import ModelWidget
from .text import TextWidget
from .union import UnionWidget


class WidgetFactory:
    def __init__(self, renderer: AbstractTemplateRenderer, token: Optional[str] = None):
        self.renderer = renderer
        self.token = token or secrets.token_urlsafe(4).replace("_", "-")

    def get_markup(
        self,
        model: ModelResult[Any],
        *,
        removable: bool,
        field: FieldInfo | None = None,
    ) -> Markup:
        return self.get_widget(
            model.model.__class__,
            model.form_data,
            model.errors,
            prefix=model.prefix,
            removable=removable,
            field=field,
        ).to_html(self.renderer)

    def get_widget(
        self,
        base: Type[Any],
        form_data: Mapping[str, Any],
        form_errors: Mapping[str, Any],
        *,
        prefix: str,
        removable: bool,
        field: FieldInfo | None = None,
    ) -> Widget[Any]:
        return self.build(
            base,
            value=form_data.get(prefix, {}),
            form_errors=form_errors,
            name=prefix,
            removable=removable,
            field=field,
        )

    def build(
        self,
        typ: Type[Any],
        *,
        name: str = "",
        value: Any,
        removable: bool,
        form_errors: Mapping[str, Any],
        field: FieldInfo | None = None,
    ) -> Widget[Any]:
        if field and field.metadata:
            for widget in field.metadata:
                if isclass(widget) and issubclass(widget, Widget):
                    return cast(
                        Widget[Any],
                        widget(
                            name,
                            value=value,
                            removable=removable,
                            title=field.title if field else "",
                            aria_label=field.description if field else None,
                            token=self.token,
                            error=form_errors.get(name),
                        ),
                    )

        type_origin = get_origin(typ)
        if type_origin:
            if is_union(typ):
                return self.build_union(name, typ, field, value, form_errors, removable)

            if (
                type_origin is Sequence
                or type_origin is MutableSequence
                or type_origin is list
            ):
                return self.build_sequence(
                    name, typ, field, value, form_errors, removable
                )

            if type_origin is Literal:
                return self.build_literal(
                    name, typ, field, value, form_errors, removable
                )

            if type_origin is set:
                return self.build_set(name, typ, field, value, form_errors, removable)

        if issubclass(typ, Enum):  # if it raises here, the type_origin is unknown
            return self.build_enum(name, typ, field, value, form_errors, removable)

        if issubclass(typ, BaseModel):  # if it raises here, the type_origin is unknown
            return self.build_model(
                name, typ, field, value or {}, form_errors, removable
            )

        if issubclass(typ, bool):
            return self.build_boolean(
                name, typ, field, value or False, form_errors, removable
            )

        if issubclass(typ, EmailStr):  # type: ignore
            return self.build_emailtype(
                name, typ, field, value or "", form_errors, removable
            )

        if issubclass(typ, SecretStr):
            return self.build_secretstr(
                name, typ, field, value or "", form_errors, removable
            )

        if issubclass(typ, (int, str, float, Decimal, UUID)):
            return self.build_simpletype(
                name, typ, field, value or "", form_errors, removable
            )

        raise NotImplementedError(f"{typ} not implemented")  # coverage: ignore

    def build_model(
        self,
        field_name: str,
        typ: Type[BaseModel],
        field: Optional[FieldInfo],
        value: Mapping[str, Any],
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        ret: dict[str, Any] = {}
        for key, field in typ.model_fields.items():
            child_key = f"{field_name}.{key}" if field_name else key
            if field.exclude:
                continue
            if field.annotation is None:
                raise ValueError(  # coverage: ignore
                    f"Missing annotation for {field} in {child_key}"
                )
            ret[key] = self.build(
                field.annotation,
                name=child_key,
                field=field,
                value=value.get(key),
                form_errors=form_errors,
                removable=False,
            )
        return ModelWidget(
            field_name,
            value=list(ret.values()),
            removable=removable,
            title=get_title(typ),
            token=self.token,
            error=form_errors.get(field_name),
        )

    def build_union(
        self,
        field_name: str,
        field_type: Type[Any],
        field: Optional[FieldInfo],
        value: Any,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        types: list[Type[Any]] = []
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
            token=self.token,
            removable=removable,
            error=form_errors.get(field_name),
        )

        return widget

    def build_sequence(
        self,
        field_name: str,
        field_type: Type[Any],
        field: Optional[FieldInfo],
        value: Optional[Sequence[Any]],
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
            hint=field.description if field else "",
            title=field.title if field else "",
            value=items,
            item_type=typ,  # type: ignore
            token=self.token,
            removable=removable,
            error=form_errors.get(field_name),
        )

    def build_set(
        self,
        field_name: str,
        field_type: Type[Any],
        field: Optional[FieldInfo],
        value: Optional[Sequence[Any]],
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
                raise NotImplementedError
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
            raise NotImplementedError

        return ChecklistWidget(
            field_name,
            title=field.title if field else "",
            token=self.token,
            value=choices,
            removable=removable,
            error=form_errors.get(field_name),
        )

    def build_boolean(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: bool,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return BooleanWidget(
            field_name,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=value,
            error=form_errors.get(field_name),
        )

    def build_emailtype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return TextWidget(
            field_name,
            hint=field.description if field else "",
            input_type="email",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )

    def build_secretstr(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: SecretStr | str,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return TextWidget(
            field_name,
            hint=field.description if field else "",
            input_type="password",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=value.get_secret_value() if isinstance(value, SecretStr) else value,
            error=form_errors.get(field_name),
        )

    def build_literal(
        self,
        field_name: str,
        field_type: Type[Any],  # a literal actually
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
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )

    def build_enum(
        self,
        field_name: str,
        field_type: Type[Any],  # an enum subclass
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
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )

    def build_simpletype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        return TextWidget(
            field_name,
            hint=field.description if field else None,
            placeholder=str(field.examples[0]) if field and field.examples else None,
            aria_label=field.description if field else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=str(value),
            error=form_errors.get(field_name),
        )
