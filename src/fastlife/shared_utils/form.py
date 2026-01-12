"""HTML Form helpers."""

from collections.abc import Sequence
from inspect import isclass
from typing import Any, get_args, get_origin

from pydantic import BaseModel, ValidationError

from fastlife.shared_utils.infer import (
    get_runtime_type,
    get_type_by_discriminator,
    is_union,
)


def flatten_error(
    exc: ValidationError, prefix: str, pydantic_model: type[Any]
) -> dict[str, str]:
    """
    Flatten a Pydantic ValidationError into a dictionary of error messages.

    The dict returned use the same key as the way
    :meth:`pydantic_form <fastlife.adapters.xcomponent.renderer.XRendererFactory.pydantic_form>`
    serialized its data, in order to display error message on appropriate fields
    on the html representation.

    :param exc: The ValidationError exception containing validation errors
    :param prefix: The initial prefix/path for the error location
    :param pydantic_model: The Pydantic model class being validated
    :return: Dictionary mapping error locations to error messages
    """
    errors: dict[str, str] = {}
    typ: Any
    runtime_type: Any = get_runtime_type(pydantic_model)
    for error in exc.errors():
        loc = prefix
        typ = runtime_type
        locations = iter(error["loc"])
        while True:
            part = next(locations, None)
            if part is None:
                # safety break that should not happen
                break  # coverage: ignore
            if isinstance(part, str):
                assert isclass(typ) and issubclass(typ, BaseModel)  # type: ignore
                field = typ.model_fields[part]
                typ = field.annotation
                type_origin = get_origin(typ)
                if type_origin:
                    if is_union(typ):
                        assert isinstance(field.discriminator, str)
                        loc = f"{loc}.{part}"
                        part = next(locations, None)
                        if part is None:
                            break
                        typ = get_type_by_discriminator(part, field.discriminator, typ)
                        assert typ is not None  # pydantic never let you get None here
                    else:
                        loc = f"{loc}.{part}"
                elif issubclass(typ, BaseModel):
                    loc = f"{loc}.{part}"
                else:
                    # the last attribute
                    loc = f"{loc}.{part}"
                    break
            else:
                # we are in a sequence
                loc = f"{loc}.{part}"
                type_origin = get_origin(typ)
                assert type_origin and issubclass(type_origin, Sequence)
                typ = get_args(typ)[0]

        if loc in errors:
            errors[loc] = f"{errors[loc]}, {error['msg']}"
        else:
            errors[loc] = error["msg"]
    return errors
