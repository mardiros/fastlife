from typing import Any, Callable, Generic, Mapping, Type, TypeVar, get_origin

from fastapi import Depends
from pydantic import BaseModel, ValidationError

from fastlife.configurator.registry import Registry
from fastlife.request.form_data import MappingFormData
from fastlife.shared_utils.infer import is_union

T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


class ModelResult(Generic[T]):
    prefix: str
    model: T
    errors: Mapping[str, str]
    is_valid: bool

    def __init__(
        self, prefix: str, model: T, errors: Mapping[str, Any], is_valid: bool = False
    ) -> None:
        self.prefix = prefix
        self.model = model
        self.errors = errors
        self.is_valid = is_valid

    @classmethod
    def default(cls, prefix: str, pydantic_type: Type[T]) -> "ModelResult[T]":
        return cls(prefix, pydantic_type.model_construct(), {})

    @property
    def form_data(self) -> Mapping[str, Any]:
        return {self.prefix: self.model.model_dump()}

    @classmethod
    def from_payload(
        cls, prefix: str, pydantic_type: Type[T], data: Mapping[str, Any]
    ) -> "ModelResult[T]":
        try:
            return cls(prefix, pydantic_type(**data.get(prefix, {})), {}, True)
        except ValidationError as exc:
            errors: dict[str, str] = {}
            for error in exc.errors():
                loc = prefix
                typ: Any = pydantic_type
                for part in error["loc"]:
                    if isinstance(part, str):
                        type_origin = get_origin(typ)
                        if type_origin:
                            if is_union(typ):
                                args = typ.__args__
                                for arg in args:
                                    if arg.__name__ == part:
                                        typ = arg
                                        continue

                            else:
                                raise NotImplementedError
                        elif issubclass(typ, BaseModel):
                            typ = typ.model_fields[part].annotation
                            loc = f"{loc}.{part}"
                        else:
                            raise NotImplementedError

                    else:
                        # it is an integer and it part of the list
                        loc = f"{loc}.{part}"

                if loc in errors:
                    errors[loc] = f"{errors[loc]}, {error['msg']}"
                else:
                    errors[loc] = error["msg"]
            model = pydantic_type.model_construct(**data.get(prefix, {}))
            return cls(prefix, model, errors)


def model(
    cls: Type[T], name: str | None = None
) -> Callable[[Mapping[str, Any]], ModelResult[T]]:
    """
    Build a model, a class of type T based on Pydandic Base Model from a form payload.
    """

    def to_model(data: MappingFormData, registry: Registry) -> ModelResult[T]:
        prefix = name or registry.settings.form_data_model_prefix
        if not data:
            return ModelResult[T].default(prefix, cls)
        return ModelResult[T].from_payload(prefix, cls, data)

    return Depends(to_model)
