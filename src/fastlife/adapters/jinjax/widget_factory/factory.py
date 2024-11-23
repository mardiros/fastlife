"""
Create markup for pydantic forms.
"""

import secrets
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, get_origin

from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import CustomWidget, Widget
from fastlife.domain.model.form import FormModel
from fastlife.domain.model.template import JinjaXTemplate

if TYPE_CHECKING:
    from fastlife.service.templates import AbstractTemplateRenderer

from .base import BaseWidgetBuilder
from .bool_builder import BoolBuilder
from .emailstr_builder import EmailStrBuilder
from .enum_builder import EnumBuilder
from .literal_builder import LiteralBuilder
from .model_builder import ModelBuilder
from .secretstr_builder import SecretStrBuilder
from .sequence_builder import SequenceBuilder
from .set_builder import SetBuilder
from .simpletype_builder import SimpleTypeBuilder
from .union_builder import UnionBuilder


class FatalError(JinjaXTemplate):
    template = """<pydantic_form.FatalError :message="message" />"""
    message: str


class WidgetFactory:
    """
    Form builder for pydantic model.

    :param renderer: template engine to render widget.
    :param token: reuse a token.
    """

    def __init__(self, renderer: "AbstractTemplateRenderer", token: str | None = None):
        self.renderer = renderer
        self.token = token or secrets.token_urlsafe(4).replace("_", "-")
        self.builders: list[BaseWidgetBuilder[Any]] = [
            # Order is super important here
            # starts by the union type
            UnionBuilder(self),
            # and to other types that have an origin
            SetBuilder(self),
            LiteralBuilder(self),
            SequenceBuilder(self),
            # from this part, order does not really matter
            ModelBuilder(self),
            BoolBuilder(self),
            EnumBuilder(self),
            EmailStrBuilder(self),
            SecretStrBuilder(self),
            # we keep simple types, str, int at the end
            SimpleTypeBuilder(self),
        ]

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
        ret = Markup()
        if model.fatal_error:
            ret += self.renderer.render_template(FatalError(message=model.fatal_error))
        ret += self.get_widget(
            model.model.__class__,
            model.form_data,
            model.errors,
            prefix=model.prefix,
            removable=removable,
            field=field,
        ).to_html(self.renderer)
        return ret

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
                if isinstance(widget, CustomWidget):
                    ret: Widget[Any] = widget.typ(
                        name=name,
                        value=value,
                        removable=removable,
                        title=field.title or "" if field else "",
                        hint=field.description if field else None,
                        aria_label=(
                            field.json_schema_extra.get("aria_label")  # type:ignore
                            if field and field.json_schema_extra
                            else None
                        ),
                        token=self.token,
                        error=form_errors.get(name),
                    )
                    return ret

        type_origin = get_origin(typ)
        for builder in self.builders:
            if builder.accept(typ, type_origin):
                return builder.build(
                    field_name=name,
                    field_type=typ,
                    field=field,
                    value=value,
                    form_errors=form_errors,
                    removable=removable,
                )

        raise NotImplementedError(f"{typ} not implemented")  # coverage: ignore
