"""Type inference."""

import inspect
from collections.abc import Callable
from types import UnionType
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel

from fastlife.domain.model.template import InlineTemplate


def is_complex_type(typ: type[Any]) -> bool:
    """
    Used to detect complex type such as Mapping, Sequence and pydantic BaseModel.

    This method cannot be used outside pydantic serialization.
    """
    return bool(get_origin(typ) or issubclass(typ, BaseModel))


def is_union(typ: type[Any]) -> bool:
    """Used to detect unions like Optional[T], Union[T, U] or T | U."""
    type_origin = get_origin(typ)
    if type_origin:
        if type_origin is Union:  # Optional[T]
            return True

        if type_origin is UnionType:  # T | U
            return True
    return False


def is_inline_template_returned(endpoint: Callable[..., Any]) -> bool:
    """Test if a view, the endpoint return a template."""
    signature = inspect.signature(endpoint)
    return_annotation = signature.return_annotation

    if isinstance(return_annotation, type) and issubclass(
        return_annotation, InlineTemplate
    ):
        return True

    if is_union(return_annotation):
        return any(
            isinstance(arg, type) and issubclass(arg, InlineTemplate)
            for arg in get_args(return_annotation)
        )

    return False
