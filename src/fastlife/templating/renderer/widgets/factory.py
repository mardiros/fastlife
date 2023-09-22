from decimal import Decimal
from typing import Any, Mapping, Optional, Type

from markupsafe import Markup
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from fastlife.templating.renderer.abstract import AbstractTemplateRenderer

from .base import Widget, get_title
from .model import ModelWidget
from .text import TextWidget


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
    ) -> Widget:
        if issubclass(typ, BaseModel):
            return self.build_model(name, typ, field, value or {})

        assert field is not None

        if issubclass(typ, (int, str, float, Decimal)):
            return self.build_simpletype(name, typ, field, value or "")
        raise NotImplementedError(f"{typ} not implemented")

    def build_model(
        self,
        field_name: str,
        typ: Type[BaseModel],
        field: Optional[FieldInfo],
        value: Mapping[str, Any],
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
        )

    def build_simpletype(
        self,
        field_name: str,
        field_type: Type[Any],
        field: FieldInfo,
        value: str | int | float,
    ) -> Widget:
        return TextWidget(
            field_name,
            title=field.title,
            placeholder=str(field.examples[0]) if field.examples else None,
            help_text=field.description,
            value=str(value),
        )
