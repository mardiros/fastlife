from types import UnionType
from typing import Any, Type, Union, get_origin

from pydantic import BaseModel


def is_complex_type(typ: Type[Any]) -> bool:
    return bool(get_origin(typ) or issubclass(typ, BaseModel))


def is_union(typ: Type[Any]) -> bool:
    type_origin = get_origin(typ)
    if type_origin:
        if type_origin is Union:  # Optional[T]
            return True

        if type_origin is UnionType:  # T | U
            return True
    return False
