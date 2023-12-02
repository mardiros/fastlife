import secrets
from collections.abc import MutableSequence, Sequence
from decimal import Decimal
from types import NoneType
from typing import Any, Literal, Mapping, Optional, Type, get_origin

from markupsafe import Markup
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from pydantic.fields import FieldInfo

from fastlife.shared_utils.infer import is_complex_type, is_union
from fastlife.templating.renderer.abstract import AbstractTemplateRenderer
from fastlife.templating.renderer.widgets.boolean import BooleanWidget
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

    async def get_markup(
        self,
        base: Type[Any],
        form_data: Mapping[str, Any],
        *,
        prefix: str,
        removable: bool,
    ) -> Markup:
        return await self.get_widget(
            base, form_data, prefix=prefix, removable=removable
        ).to_html(self.renderer)

    def get_widget(
        self,
        base: Type[Any],
        form_data: Mapping[str, Any],
        *,
        prefix: str,
        removable: bool,
    ) -> Widget:
        return self.build(
            base, value=form_data.get(prefix, {}), name=prefix, removable=removable
        )

    def build(
        self,
        typ: Type[Any],
        *,
        name: str = "",
        value: Any,
        removable: bool,
        field: Optional[FieldInfo] = None,
    ) -> Widget:
        type_origin = get_origin(typ)
        if type_origin:
            if is_union(typ):
                return self.build_union(name, typ, field, value, removable)

            if (
                type_origin is Sequence
                or type_origin is MutableSequence
                or type_origin is list
            ):
                return self.build_sequence(name, typ, field, value, removable)

            if type_origin is Literal:
                return self.build_literal(name, typ, field, value, removable)

        if issubclass(typ, BaseModel):  # if it raises here, the type_origin is unknown
            return self.build_model(name, typ, field, value or {}, removable)

        if issubclass(typ, (bool)):
            return self.build_boolean(name, typ, field, value or False, removable)

        if issubclass(typ, EmailStr):
            return self.build_emailtype(name, typ, field, value or "", removable)

        if issubclass(typ, SecretStr):
            return self.build_secretstr(name, typ, field, value or "", removable)

        if issubclass(typ, (int, str, float, Decimal)):
            return self.build_simpletype(name, typ, field, value or "", removable)

        raise NotImplementedError(f"{typ} not implemented")

    def build_model(
        self,
        field_name: str,
        typ: Type[BaseModel],
        field: Optional[FieldInfo],
        value: Mapping[str, Any],
        removable: bool,
    ) -> Widget:
        ret: dict[str, Any] = {}
        for key, field in typ.model_fields.items():
            child_key = f"{field_name}.{key}" if field_name else key
            if field.exclude:
                continue
            if field.annotation is None:
                raise ValueError(f"Missing annotation for {field} in {child_key}")
            ret[key] = self.build(
                field.annotation,
                name=child_key,
                field=field,
                value=value.get(key),
                removable=False,
            )
        return ModelWidget(
            field_name,
            children_widget=list(ret.values()),
            removable=removable,
            title=get_title(typ),
            token=self.token,
        )

    def build_union(
        self,
        field_name: str,
        field_type: Type[Any],
        field: Optional[FieldInfo],
        value: Any,
        removable: bool,
    ) -> Widget:
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
                types[0], name=field_name, field=field, value=value, removable=False
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
                        removable=False,
                    )

        widget = UnionWidget(
            field_name,
            # we assume those types are BaseModel
            child=child,
            children_types=types,  # type: ignore
            title=field.title if field else "",
            token=self.token,
            removable=removable,
        )

        return widget

    def build_sequence(
        self,
        field_name: str,
        field_type: Type[Any],
        field: Optional[FieldInfo],
        value: Optional[Sequence[Any]],
        removable: bool,
    ) -> Widget:
        typ = field_type.__args__[0]  # type: ignore
        value = value or []
        items = [
            self.build(
                typ,  # type: ignore
                name=f"{field_name}.{idx}",
                value=v,
                field=field,
                removable=True,
            )
            for idx, v in enumerate(value)
        ]
        return SequenceWidget(
            field_name,
            help_text=field.description if field else "",
            title=field.title if field else "",
            items=items,
            item_type=typ,  # type: ignore
            token=self.token,
            removable=removable,
        )

    def build_boolean(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: bool,
        removable: bool,
    ) -> Widget:
        return BooleanWidget(
            field_name,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=value,
        )

    def build_emailtype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        removable: bool,
    ) -> Widget:
        return TextWidget(
            field_name,
            help_text=field.description if field else "",
            input_type="email",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=str(value),
        )

    def build_secretstr(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: SecretStr | str,
        removable: bool,
    ) -> Widget:
        return TextWidget(
            field_name,
            help_text=field.description if field else "",
            input_type="password",
            placeholder=str(field.examples[0]) if field and field.examples else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=value.get_secret_value() if isinstance(value, SecretStr) else value,
        )

    def build_literal(
        self,
        field_name: str,
        field_type: Type[Any],  # a literal actually
        field: FieldInfo | None,
        value: str | int | float,
        removable: bool,
    ) -> Widget:
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
        )

    def build_simpletype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo | None,
        value: str | int | float,
        removable: bool,
    ) -> Widget:
        return TextWidget(
            field_name,
            help_text=field.description if field else None,
            placeholder=str(field.examples[0]) if field and field.examples else None,
            aria_label=field.description if field else None,
            removable=removable,
            title=field.title if field else "",
            token=self.token,
            value=str(value),
        )
