"""Type inference."""

from types import UnionType
from typing import Any, Union, get_origin

from pydantic import BaseModel


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
