"""HTTP Form serialization."""

from collections.abc import Mapping
from typing import Any, Generic, TypeVar, get_origin

from pydantic import BaseModel, ValidationError

from fastlife.shared_utils.infer import is_union

T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


class FormModel(Generic[T]):
    prefix: str
    model: T
    fatal_error: str
    errors: dict[str, str]
    is_valid: bool

    def __init__(
        self, prefix: str, model: T, errors: dict[str, Any], is_valid: bool = False
    ) -> None:
        self.prefix = prefix
        self.model = model
        self.fatal_error = ""
        self.errors = errors
        self.is_valid = is_valid

    @classmethod
    def default(cls, prefix: str, pydantic_type: type[T]) -> "FormModel[T]":
        return cls(prefix, pydantic_type.model_construct(), {})

    def set_fatal_error(self, value: str) -> None:
        self.fatal_error = value
        self.is_valid = False

    def add_error(self, field: str, value: str) -> None:
        self.errors[f"{self.prefix}.{field}"] = value
        self.is_valid = False

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
            ret = cls(prefix, pydantic_type(**data.get(prefix, {})), {}, True)
            return ret
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
