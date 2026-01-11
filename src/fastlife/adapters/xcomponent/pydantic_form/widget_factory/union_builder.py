"""Handle Union type."""

from collections.abc import Mapping
from types import NoneType
from typing import Annotated, Any, get_args, get_origin

from pydantic import ValidationError, create_model
from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.base import (
    BaseWidgetBuilder,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.base import Widget
from fastlife.adapters.xcomponent.pydantic_form.widgets.union import UnionWidget
from fastlife.shared_utils.infer import is_complex_type, is_union


def get_title(typ: type[Any]) -> str:
    title = typ.__name__
    if get_origin(typ) is Annotated:
        base, *meta = get_args(typ)
        title = base.__name__
        for arg in meta:
            if isinstance(arg, str):
                title = arg
                break
    return title


def get_title_from_discriminator(discriminator: str, unionfield: FieldInfo) -> str:
    # we assume we have unionfield.discriminator here,
    # and we may have not
    assert unionfield.annotation
    child_name = discriminator
    for child_typ in unionfield.annotation.__args__:
        title = get_title(child_typ)
        if get_origin(child_typ) is Annotated:
            child_typ = get_args(child_typ)[0]
        if (
            discriminator
            in child_typ.model_fields[unionfield.discriminator].annotation.__args__
        ):
            child_name = title
    return child_name


def get_type_from_discriminator(discriminator: str | int, unionfield: FieldInfo) -> Any:
    # we assume we have unionfield.discriminator here,
    # and we may have not
    assert unionfield.annotation
    for child_typ in unionfield.annotation.__args__:
        if get_origin(child_typ) is Annotated:
            child_typ = get_args(child_typ)[0]
        if (
            discriminator
            in child_typ.model_fields[unionfield.discriminator].annotation.__args__
        ):
            return child_typ
    return None


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
        types: dict[type[Any], str] = {}
        # required = True
        # # breakpoint()
        for typ in field_type.__args__:  # type: ignore
            if typ is NoneType:
                # required = False
                continue

            title = get_title(typ)
            if get_origin(typ) is Annotated:
                typ = get_args(typ)[0]

            types[typ] = title

        if (
            not removable
            and len(types) == 1
            # if the optional type is a complex type,
            and not is_complex_type(next(iter(types.keys())))
        ):
            return self.factory.build(  # coverage: ignore
                next(iter(types.keys())),
                name=field_name,
                field=field,
                value=value,
                form_errors=form_errors,
                removable=False,
            )
        child = None
        if value:
            assert field and field.annotation and isinstance(field.discriminator, str)
            DynamicModel = create_model("DynamicModel", value=(field.annotation, field))
            try:
                submod = DynamicModel(value=value)
                discriminator = getattr(submod, field.discriminator)
            except ValidationError as exc:
                submod = DynamicModel.model_construct(value=value)
                discriminator = exc.errors()[0]["loc"][1]
                typ = get_type_from_discriminator(discriminator, field)

            child = self.factory.build(
                typ,
                name=field_name,
                field=FieldInfo(
                    title=get_title_from_discriminator(discriminator, field)
                ),
                value=submod.value,  # type: ignore
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
            children_types={v: k for k, v in types.items()},
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
