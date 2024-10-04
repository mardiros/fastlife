"""HTTP Form serialization."""

from collections.abc import Callable, Mapping
from typing import Any, Generic, TypeVar, get_origin

from fastapi import Depends
from pydantic import BaseModel, ValidationError

from fastlife import Registry
from fastlife.request.form_data import MappingFormData
from fastlife.shared_utils.infer import is_union

T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


class FormModel(Generic[T]):
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
    def default(cls, prefix: str, pydantic_type: type[T]) -> "FormModel[T]":
        return cls(prefix, pydantic_type.model_construct(), {})

    def edit(self, pydantic_type: T) -> None:
        """
        Load the form with the given model and consider it as valid for the user.

        No error will be reported.
        """
        self.model = pydantic_type
        self.errors = {}
        self.is_valid = True

    @property
    def form_data(self) -> Mapping[str, Any]:
        return {self.prefix: self.model.model_dump()}

    @classmethod
    def from_payload(
        cls, prefix: str, pydantic_type: type[T], data: Mapping[str, Any]
    ) -> "FormModel[T]":
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
                                raise NotImplementedError from exc  # coverage: ignore
                        elif issubclass(typ, BaseModel):
                            typ = typ.model_fields[part].annotation
                            loc = f"{loc}.{part}"
                        else:
                            raise NotImplementedError from exc  # coverage: ignore

                    else:
                        # it is an integer and it part of the list
                        loc = f"{loc}.{part}"

                if loc in errors:
                    errors[loc] = f"{errors[loc]}, {error['msg']}"
                else:
                    errors[loc] = error["msg"]
            model = pydantic_type.model_construct(**data.get(prefix, {}))
            return cls(prefix, model, errors)


def form_model(
    cls: type[T], name: str | None = None
) -> Callable[[Mapping[str, Any]], FormModel[T]]:
    """
    Build a model, a class of type T based on Pydandic Base Model from a form payload.
    """

    def to_model(data: MappingFormData, registry: Registry) -> FormModel[T]:
        prefix = name or registry.settings.form_data_model_prefix
        if not data:
            return FormModel[T].default(prefix, cls)
        return FormModel[T].from_payload(prefix, cls, data)

    return Depends(to_model)
