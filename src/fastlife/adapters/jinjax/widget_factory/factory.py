"""
Create markup for pydantic forms.
"""

import secrets
from collections.abc import Mapping, MutableSequence, Sequence
from decimal import Decimal
from enum import Enum
from inspect import isclass
from typing import Any, Literal, cast, get_origin
from uuid import UUID

from markupsafe import Markup
from pydantic import BaseModel, EmailStr, SecretStr
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.request.form import FormModel
from fastlife.services.templates import AbstractTemplateRenderer
from fastlife.shared_utils.infer import is_union

from .builtin_factory import BuiltinFactoryMixin
from .enum_factory import EnumFactoryMixin
from .model_factory import ModelFactoryMixin
from .sequence_factory import SequenceFactoryMixin
from .union_factory import UnionFactoryMixin


class WidgetFactory(
    ModelFactoryMixin,
    UnionFactoryMixin,
    SequenceFactoryMixin,
    EnumFactoryMixin,
    BuiltinFactoryMixin,
):
    """
    Form builder for pydantic model.

    :param renderer: template engine to render widget.
    :param token: reuse a token.
    """

    def __init__(self, renderer: AbstractTemplateRenderer, token: str | None = None):
        self.renderer = renderer
        self.token = token or secrets.token_urlsafe(4).replace("_", "-")

    def get_markup(
        self,
        model: FormModel[Any],
        *,
        removable: bool = False,
        field: FieldInfo | None = None,
    ) -> Markup:
        """
        Get the markup for the given model.

        :param model: the model to build the html markup.
        :param removable: Include a button to remove the model in the markup.
        :param field: only build the markup of this field is not None.
        """
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
        base: type[Any],
        form_data: Mapping[str, Any],
        form_errors: Mapping[str, Any],
        *,
        prefix: str,
        removable: bool,
        field: FieldInfo | None = None,
    ) -> Widget[Any]:
        """
        build the widget for the given type and return it.
        :param base: the type to build, it has to be a builtin or a Pydantic model.
        :param form_data: form values to render.
        :param form_errors: form errors to render.
        """
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
        typ: type[Any],
        *,
        name: str = "",
        value: Any,
        removable: bool,
        form_errors: Mapping[str, Any],
        field: FieldInfo | None = None,
    ) -> Widget[Any]:
        """
        build widget tree for the given type.
        This function is recurive and shoud not be used directly.
        The type is a composite, it can be pydantic model, builtin, list or unions.

        The {meth}`WidgetFactory.get_widget` or {meth}`WidgetFactory.get_markup`
        should be used.

        :param typ: the type to build, it has to be a builtin or a Pydantic model.
        :param name: name of the widget to build.
        :param value: value for the widget.
        :param removable: True if it has to include a remove button.
        :param form_errors: errors in the form.
        :param field: field information used to customize the widget.
        """
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
                            hint=field.description if field else None,
                            aria_label=(
                                field.json_schema_extra.get("aria_label")  # type:ignore
                                if field and field.json_schema_extra
                                else None
                            ),
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

        if issubclass(typ, int | str | float | Decimal | UUID):
            return self.build_simpletype(
                name, typ, field, value or "", form_errors, removable
            )

        raise NotImplementedError(f"{typ} not implemented")  # coverage: ignore
