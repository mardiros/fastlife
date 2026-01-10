"""Handle Union type."""

from collections.abc import Mapping
from types import NoneType
from typing import Annotated, Any, get_args, get_origin

from pydantic import ValidationError
from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.base import (
    BaseWidgetBuilder,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.base import Widget
from fastlife.adapters.xcomponent.pydantic_form.widgets.union import UnionWidget
from fastlife.shared_utils.infer import is_complex_type, is_union


class UnionBuilder(BaseWidgetBuilder[Any]):
    """Builder for Union."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for unions Union[A,B], A | B or event Optional[A], A | None"""
        return is_union(typ)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: Any | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[Any]:
        """Build the widget."""
        title = ""
        types: dict[str, type[Any]] = {}
        # required = True
        # breakpoint()
        for typ in field_type.__args__:  # type: ignore
            if typ is NoneType:
                # required = False
                continue

            title = typ.__name__
            if get_origin(typ) is Annotated:
                base, *meta = get_args(typ)
                title = base.__name__
                for arg in meta:
                    if isinstance(arg, str):
                        title = arg
                        break
                typ = base
            types[title] = typ  # type: ignore

        if (
            not removable
            and len(types) == 1
            # if the optional type is a complex type,
            and not is_complex_type(types[title])
        ):
            return self.factory.build(  # coverage: ignore
                types[title],
                name=field_name,
                field=field,
                value=value,
                form_errors=form_errors,
                removable=False,
            )
        child = None
        if value:
            for typ in types.values():
                try:
                    typ(**value)
                except ValidationError:
                    pass
                else:
                    child = self.factory.build(
                        typ,
                        name=field_name,
                        field=field,
                        value=value,
                        form_errors=form_errors,
                        removable=False,
                    )

        # FIXME Union[Sequence[FooModel]]
        # if isinstance(child, Sequence):
        #     child = child.__args__[0]

        widget = UnionWidget[Any](
            name=field_name,
            # we assume those types are BaseModel
            value=child,
            children_types=types,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            removable=removable,
            error=form_errors.get(field_name),
        )

        return widget
