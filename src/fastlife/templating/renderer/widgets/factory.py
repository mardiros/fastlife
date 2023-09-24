from decimal import Decimal
from types import NoneType, UnionType
from typing import Any, Mapping, Optional, Type, Union, get_origin
from xmlrpc.client import boolean

from markupsafe import Markup
from pydantic import BaseModel, EmailStr
from pydantic.fields import FieldInfo

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget

from .base import Widget, get_title
from .model import ModelWidget
from .text import TextWidget
from .union import UnionWidget


def is_complex_type(typ: Type[Any]) -> bool:
    return get_origin(typ) or issubclass(typ, BaseModel)


class WidgetFactory:
    def __init__(self, renderer: AbstractTemplateRenderer):
        self.renderer = renderer

    async def get_markup(
        self,
        base: Type[BaseModel],
        form_data: Mapping[str, Any],
        prefix: str = "payload",
    ) -> Markup:
        return await self.get_widget(base, form_data, prefix=prefix).to_html(
            self.renderer
        )

    def get_widget(
        self,
        base: Type[BaseModel],
        form_data: Mapping[str, Any],
        prefix: str,
    ) -> Widget:
        return self.build(base, value=form_data.get(prefix, {}), name=prefix)

    def build(
        self,
        typ: Type[Any],
        *,
        name: str = "",
        value: Any,
        field: Optional[FieldInfo] = None,
        required: boolean = True,
    ) -> Widget:
        type_origin = get_origin(typ)
        if type_origin:
            assert field is not None

            if (
                type_origin is Union  # Optional[T]
                or type_origin is UnionType  # T | None
            ):
                return self.build_union(name, typ, field, value, required)

        if issubclass(typ, BaseModel):
            return self.build_model(name, typ, field, value or {}, required)

        assert field is not None

        if issubclass(typ, (bool)):
            return self.build_boolean(name, typ, field, value or False, required)

        if issubclass(typ, EmailStr):
            return self.build_emailtype(name, typ, field, value or "", required)

        if issubclass(typ, (int, str, float, Decimal)):
            return self.build_simpletype(name, typ, field, value or "", required)

        raise NotImplementedError(f"{typ} not implemented")

    def build_model(
        self,
        field_name: str,
        typ: Type[BaseModel],
        field: Optional[FieldInfo],
        value: Mapping[str, Any],
        required: bool,
    ) -> Widget:
        ret: dict[str, Any] = {}
        for key, field in typ.model_fields.items():
            child_key = f"{field_name}.{key}" if field_name else key
            if field.exclude:
                continue
            if field.annotation is None:
                raise ValueError(f"Missing annotation for {field} in {child_key}")
            ret[key] = self.build(
                field.annotation, name=child_key, field=field, value=value.get(key)
            )
        return ModelWidget(
            field_name,
            title=get_title(typ),
            children_widget=list(ret.values()),
            required=required,
        )

    def build_union(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo,
        value: Any,
        required: bool,
    ) -> Widget:
        types: list[Type[Any]] = []
        required = True
        for typ in field_type.__args__:  # type: ignore
            if typ is NoneType:
                required = False
                continue
            types.append(typ)  # type: ignore

        if (
            not required
            and len(types) == 1
            # if the optional type is a complex type,
            and not is_complex_type(types[0])
        ):
            return self.build(
                types[0], name=field_name, field=field, value=value, required=True
            )

        widget = UnionWidget(
            child=None,
            children_types=types,
        )

        return widget

    def build_boolean(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo,
        value: bool,
        required: bool,
    ) -> Widget:
        return BooleanWidget(
            field_name, title=field.title, value=value, required=required
        )

    def build_emailtype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo,
        value: str | int | float,
        required: bool,
    ) -> Widget:
        return TextWidget(
            field_name,
            title=field.title,
            placeholder=str(field.examples[0]) if field.examples else None,
            help_text=field.description,
            value=str(value),
            required=required,
            input_type="email",
        )

    def build_simpletype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo,
        value: str | int | float,
        required: bool,
    ) -> Widget:
        return TextWidget(
            field_name,
            title=field.title,
            placeholder=str(field.examples[0]) if field.examples else None,
            help_text=field.description,
            value=str(value),
            required=required,
        )
